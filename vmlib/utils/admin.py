import datetime
import math
import pathlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import squarify
import vmlib as vm
from .. plot.styles import set_plot_styles


def load_log_file(params):
    # Parse parameters and load excel in dataframes
    vm.utils.print.info('Start - data loading', 1)
    params = _parse_params(params)
    log, activities, holidays, paid = _load_sheets(params)
    # Format date time, clean project names, fill status and class cat/sub_cat
    log = _compile_datetime(log)
    log = _clean_project(log)
    log['type'] = log.apply(lambda row: _define_type(row), axis=1)
    log = _split_cat(log, activities)
    vm.utils.print.info('End - data loading', 1)
    # Create daily summary dataframe
    vm.utils.print.info('Start - create daily summary', 1)
    # Initialize df and get weekday, weekday_cat, expect. work, excess ratio
    daily = _init_daily_df(log)
    daily = _get_expected_work(daily, params, holidays)
    daily.set_index('day', inplace=True)
    # Get daily quantities (Total, holidays, work)
    daily = pd.concat([daily, _get_day_quantities(log)], axis=1)
    # Compute holidays (round 0.5), compensated days, recuperation days
    daily['taken_days'] = daily.apply(lambda row: _compute_holidays(row,
                                                                    params),
                                      axis=1)
    daily['taken_days'] = daily.apply(lambda row: _compensated(row, paid),
                                      axis=1)
    daily['recup_days'] = daily.apply(lambda row: _recup(row, params),
                                      axis=1)
    # Compute expected work (corrected for holidays and recup) and excess time
    daily['expected_work'] = daily.apply(lambda row: _expected(row, params),
                                         axis=1)
    daily['supp_work'] = daily['work_duration'] - daily['expected_work']
    # Convert to hours
    daily['work_hours'] = round(daily['work_duration'] / 3600, 1)
    daily['supp_hours'] = round(daily['supp_work'] / 3600, 1)
    # Compute balance
    daily['supp_balance'] = daily['supp_hours'].cumsum()
    daily['quota'] = daily.apply(lambda row: _quota_day(row, params),
                                 axis=1)
    daily['holiday_sold'] = daily['quota'] + daily['recup_days'] - \
        daily['taken_days']
    daily['holidays'] = 4.5 + daily['holiday_sold'].cumsum().round(1)
    # Dataframe cleanup
    daily.drop(['weekday_cat', 'theo_work', 'excess_ratio', 'total_duration',
                'holidays_duration', 'expected_work', 'work_duration',
                'supp_work', 'quota', 'holiday_sold'], axis=1, inplace=True)
    daily = daily[['weekday', 'work_hours', 'supp_hours', 'supp_balance',
                   'taken_days', 'recup_days', 'holidays']]
    vm.utils.print.info('End - create daily summary', 1)
    return log, daily, holidays, activities


def get_range(daily):
    days = list(pd.Series(daily.index.format()))
    months = sorted(list(set([x[:7] for x in days])))
    years = sorted(list(set([x.split('-')[0] for x in days])))
    return months, years


def monthly_summary(month, log, daily, activities):
    vm.utils.print.info(f'Create monthly summary - {month}', 1)
    # Get month data and clean
    month_log = log[log['day'].dt.strftime('%Y-%m') == month].copy()
    month_daily = daily[daily.index.strftime('%Y-%m') == month]
    day = month_log['day'].astype(str).str[:10]
    month_log['day'] = day
    month_log.drop(['start', 'end'], axis=1, inplace=True)
    # Split by type (client vs intern)
    month_client = month_log[month_log['type'] == 'client']
    month_intern = month_log[month_log['type'] == 'intern']
    # Create summary dataframe
    main_cats = sorted(list(activities['main_cat'].unique()))
    projects = sorted(list(month_client['project'].unique()))
    totals = ['Heures', 'H. Suppl.', 'Congé', 'Récup.']
    balance = ['Vacances', 'Heures']
    ix_1 = len(projects) * ['Projets'] + len(main_cats) * ['Geo2X'] + \
        4 * ['Total'] + 2 * ['Solde']
    ix_2 = projects + main_cats + totals + balance
    days = sorted(list(month_daily.index.astype(str)))
    df = pd.DataFrame(np.zeros((len(ix_1), len(days))),
                      index=[ix_1, ix_2])
    df.columns = days
    # Fill total / balance
    month_daily = month_daily.T
    hours = list(month_daily.loc['work_hours'].values)
    supp = list(month_daily.loc['supp_hours'].values)
    supp_bal = list(month_daily.loc['supp_balance'].values)
    taken = list(month_daily.loc['taken_days'].values)
    rec = list(month_daily.loc['recup_days'].values)
    hol_bal = list(month_daily.loc['holidays'].values)
    df.loc[('Total', 'Heures'), :] = hours
    df.loc[('Total', 'H. Suppl.'), :] = supp
    df.loc[('Total', 'Congé'), :] = taken
    df.loc[('Total', 'Récup.'), :] = rec
    df.loc[('Solde', 'Vacances'), :] = hol_bal
    df.loc[('Solde', 'Heures'), :] = supp_bal
    # Fill intern
    val = month_intern.groupby(['day', 'main_cat'],
                               as_index=False).agg({
                                   'duration': 'sum'})
    val['duration'] = round(val['duration'].dt.total_seconds() / 3600, 1)
    for day in days:
        for cat in main_cats:
            sel = val[(val['day'] == day) & (val['main_cat'] == cat)]
            if len(sel) > 0:
                value = sel['duration'].values
                df.loc[('Geo2X', cat), day] = value
    # Fill client
    val = month_client.groupby(['day', 'project'],
                               as_index=False).agg({
                                   'duration': 'sum'})
    val['duration'] = round(val['duration'].dt.total_seconds() / 3600, 1)
    for day in days:
        for proj in projects:
            sel = val[(val['day'] == day) & (val['project'] == proj)]
            if len(sel) > 0:
                value = sel['duration'].values
                df.loc[('Projets', proj), day] = value
    return df


def export_month_plot(month, log, daily, activities, params):
    # Prepare Weekly data
    df = log.set_index('start')
    wk = _prepare_weekly_data(df)
    # Prepare monthly data
    mth = _prepare_monthly_data(df)
    # Prepare month data
    monthly_data = _prepare_month_data(df, month)
    # Get labels and colors from activities
    for index, row in monthly_data.iterrows():
        sel = activities[activities['cat'] == row['cat']].reset_index()
        label = sel.loc[0, 'label']
        color = sel.loc[0, 'color']
        monthly_data.loc[index, 'label'] = label
        monthly_data.loc[index, 'color'] = color
    # Prepare figure and initialize styles
    plt.style.use('ggplot')
    set_plot_styles()
    mpl.rcParams['axes.xmargin'] = 0.0
    mpl.rcParams['xtick.minor.visible'] = False
    fig = plt.figure(figsize=(18, 6), constrained_layout=True)
    gs = fig.add_gridspec(ncols=3, nrows=2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[0, 1])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[:, 2])
    months = plt.matplotlib.dates.MonthLocator(interval=3)
    dateformat = plt.matplotlib.dates.DateFormatter('%b\n%y')
    # Plot time repartition
    x = wk.index.tolist()
    y = wk['per_client'].values.tolist()
    ax1.fill_between(x, y1=y, y2=0, alpha=0.6, linewidth=1)
    ax1.plot(x, y, '-k', linewidth=0.25)
    ax1.set_ylabel('Heures client [%]')
    ax1.set_ylim([0, 100])
    ax1.xaxis.set_major_locator(months)
    ax1.xaxis.set_major_formatter(dateformat)
    # Plot holidays
    x = daily.index.tolist()
    y = daily['holidays'].values.tolist()
    ax2.fill_between(x, y1=y, y2=0, alpha=0.6, color='#6ACC64', linewidth=0.25)
    ax2.plot(x, y, '-k', linewidth=0.25)
    ax2.set_ylabel('Solde vacances [jour]')
    ax2.set_ylim([0, max(y)+5])
    ax2.xaxis.set_major_locator(months)
    ax2.xaxis.set_major_formatter(dateformat)
    # Plot cat
    x = mth.index.tolist()
    y = np.vstack([mth[col].values.tolist() for col in mth.columns])
    labels = mth.columns.values.tolist()
    # Get colors
    mn_act = activities.groupby(['main_cat']).first().drop(['cat', 'abbrev',
                                                            'label', 'color'],
                                                           axis=1)
    col = [mn_act.loc[lab, 'main_color'] for lab in labels]
    ax3.stackplot(x, y, labels=labels, colors=col, alpha=0.8)
    ax3.legend(loc='upper left')
    ax3.set_ylabel('[%]')
    ax3.set_ylim([0, 100])
    ax3.xaxis.set_major_locator(months)
    ax3.xaxis.set_major_formatter(dateformat)
    # Plot hours
    x = daily.index.tolist()
    y = daily['supp_balance'].values.tolist()
    ax4.fill_between(x, y1=y, y2=0, alpha=0.6, color='#EE854A', linewidth=1)
    ax4.plot(x, y, '-k', linewidth=0.25)
    ax4.set_ylabel('Solde heures')
    ax4.set_ylim([0, max(y)+20])
    ax4.xaxis.set_major_locator(months)
    ax4.xaxis.set_major_formatter(dateformat)
    # Plot square map for each month
    monthly_data = monthly_data[monthly_data[0] > 0]
    labels = monthly_data['label'].tolist()
    sizes = monthly_data[0].tolist()

    labels = [f'{labels[i]}\n{sizes[i]}%' for i in range(len(labels))]
    colors = monthly_data['color'].tolist()
    squarify.plot(ax=ax5, sizes=sizes, label=labels,
                  color=colors, alpha=.8, text_kwargs={'fontsize': 8})
    ax5.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)
    ax5.tick_params(axis='y', which='both', right=False,
                    left=False, labelleft=False)
    for pos in ['right', 'top', 'bottom', 'left']:
        ax5.spines[pos].set_visible(True)
    # Export
    out_path = pathlib.Path(params['out_folder'], f'{month}.jpg')
    fig.savefig(out_path)
    plt.close(fig)
    vm.utils.print.info(f'Export monthly plot - {month}', 1)
    return out_path


def export_pdf(outfile, author, results):
    # Create template instance
    doc = vm.pdf.templates.Geo2x_a4(outfile)
    # Create Title page
    doc.create_title_page(title='Geo2X - Log',
                          subtitle='Décomptes mensuels',
                          img=None,
                          author=author)
    # Add content
    months = results.keys()
    for m in months:
        doc.create_text(m, 'h1')
        # DF
        doc.create_text('Daily log', 'h2')
        doc.create_table(results[m]['df'], 'log')
        # Plot
        doc.create_page_break()
        doc.create_text('Monthly activity distribution', 'h2')
        doc.create_spacer(10)
        doc.create_image(results[m]['img'], align='CENTER', width=18,
                         height=9, caption=None)
        doc.create_page_break()
    # Save document
    doc.save()
    vm.utils.print.info(f'Export report - {doc.outfile}', 1)


def _prepare_month_data(df, month):
    mt = df.groupby([pd.Grouper(freq='M'),
                     'cat']).sum()['duration'].unstack().fillna(0)
    columns = mt.columns
    for col in columns:
        mt[col] = pd.to_timedelta(mt[col]).dt.total_seconds()
    mt['tot'] = mt.sum(axis=1)
    for col in columns:
        mt[col] = round(100*mt[col]/mt['tot'], 1)
    mt.drop(['tot'], axis=1, inplace=True)
    # Get data for this month
    mt.rename(index=lambda x: x.strftime('%Y-%m'), inplace=True)
    monthly_data = mt[mt.index == month].T.unstack().reset_index()
    return monthly_data


def _prepare_weekly_data(df):
    wk = df.groupby([pd.Grouper(freq='W'),
                    'type']).sum()['duration'].unstack().fillna(0)
    wk['client'] = pd.to_timedelta(wk['client']).dt.total_seconds()
    wk['intern'] = pd.to_timedelta(wk['intern']).dt.total_seconds()
    wk['total'] = wk['client'] + wk['intern']
    wk['per_client'] = 100*(wk['client']/wk['total'])
    wk['per_intern'] = 100-wk['per_client']
    return wk


def _prepare_monthly_data(df):
    mth = df.groupby([pd.Grouper(freq='M'),
                     'main_cat']).sum()['duration'].unstack().fillna(0)
    columns = mth.columns
    for col in columns:
        mth[col] = pd.to_timedelta(mth[col]).dt.total_seconds()
    mth['tot'] = mth.sum(axis=1)
    for col in columns:
        mth[col] = round(100*mth[col]/mth['tot'], 1)
    mth.drop(['tot'], axis=1, inplace=True)
    return mth


def _expected(row, par):
    # For working days, expected = daily_amount - hol*daily_amount
    if row['weekday_cat'] == 'A':
        return par['daily_amount'] - row['taken_days']*par['daily_amount']
    elif row['weekday_cat'] == 'B':  # recup*daily_amount
        return row['recup_days']*par['daily_amount']
    elif row['weekday_cat'] == 'C':  # 2/3*recup*daily_amount
        return (2/3)*row['recup_days']*par['daily_amount']
    return 0


def _quota_day(row, par):
    day = row.name.strftime('%d')
    if day == '01':
        return par['annual_holidays']/12
    else:
        return 0


def _compute_holidays(row, params):
    if row['weekday_cat'] == 'A':
        ratio = (row['holidays_duration']-1)/params['daily_amount']
        return math.ceil(2*ratio)/2
    else:
        return 0


def _compensated(row, paid):
    # Format paid as list of strings
    dates = list(paid.index)
    dates = [x.strftime('%Y-%m-%d') for x in dates]
    # Check if row index is in dates
    ix = row.name.strftime('%Y-%m-%d')
    if ix in dates:
        a = paid.at[pd.to_datetime(ix), 'amount']
        return a
    return row['taken_days']


def _recup(row, parameters):
    q = parameters['daily_amount']
    if row['weekday_cat'] > 'A':  # weekend and official holidays
        work_amount = row['work_duration']
        if work_amount > 0 and work_amount <= q/2:
            return 0.5*row['excess_ratio']
        elif work_amount > q/2:
            return row['excess_ratio']
        else:
            return 0
    else:  # ie standard working day
        return 0


def _get_day_quantities(log):
    # Create day column
    log['day'] = log['start'].dt.strftime('%Y-%m-%d')
    log['day'] = pd.to_datetime(log['day'], format='%Y-%m-%d')
    # Get total work
    total = log.groupby('day', as_index=False).agg({'duration': 'sum'})
    total.reset_index()
    total.set_index('day', inplace=True)
    total.columns = ['total_duration']
    total['total_duration'] = total['total_duration'].dt.total_seconds()
    # Get holiday sum
    hol = log[log['cat'] == 'Holiday'].groupby('day').agg({'duration': 'sum'})
    hol.reset_index().set_index('day', inplace=True)
    hol.columns = ['holidays_duration']
    hol['holidays_duration'] = hol['holidays_duration'].dt.total_seconds()
    # Init df
    df = _init_daily_df(log)
    df.set_index('day', inplace=True)
    # Merge dataframes
    merge = pd.concat([df, total, hol], axis=1)
    # Replace Nan by zeros
    merge.fillna(0, inplace=True)
    # Get worked amount
    merge['work_duration'] = merge['total_duration']-merge['holidays_duration']
    # Return dataframe
    return merge


def _parse_holidays(row, holidays):
    if row['day'] in holidays:
        return 'C'
    else:
        return row['weekday_cat']


def _excess_ratio(row):
    if row['weekday_cat'] == 'A':
        return 0
    elif row['weekday_cat'] == 'B':
        return 1  # Saturday compensation
    elif row['weekday_cat'] == 'C':
        return 1.5  # Sunday and official holiday compensation


def _weekday_cat(row):
    if row['weekday'] == 'Saturday':
        return 'B'
    elif row['weekday'] == 'Sunday':
        return 'C'
    else:
        return 'A'


def _theo_amount(row, params):
    if row['weekday_cat'] == 'A':
        return params['daily_amount']
    else:
        return 0


def _get_expected_work(df, params, holidays):
    # Get weekday
    df['weekday'] = df.day.dt.day_name()
    # Get expected work category
    df['weekday_cat'] = df.apply(lambda row: _weekday_cat(row), axis=1)
    # Correct for holidays
    df['weekday_cat'] = df.apply(lambda row: _parse_holidays(row, holidays),
                                 axis=1)
    # Get expected work amount
    df['theo_work'] = df.apply(lambda row: _theo_amount(row, params), axis=1)
    # Get excess ratio
    df['excess_ratio'] = df.apply(lambda row: _excess_ratio(row), axis=1)
    return df


def _init_daily_df(df):
    first_day = min(df['start'])
    first_day = datetime.datetime(first_day.year,
                                  first_day.month,
                                  first_day.day)
    last_day = max(df['end'])
    last_day = datetime.datetime(last_day.year,
                                 last_day.month,
                                 last_day.day)
    dates = pd.date_range(start=first_day, end=last_day, freq='D', name='day')
    daily = pd.DataFrame(dates)
    return daily


def _compile_date(row, var):
    year = row['Date'].year
    month = row['Date'].month
    day = row['Date'].day
    hour = row[var].hour
    minute = row[var].minute
    return datetime.datetime(year, month, day, hour, minute)


def _compile_datetime(df):
    df['start'] = df.apply(lambda row: _compile_date(row, 'Start time'),
                           axis=1)
    df['end'] = df.apply(lambda row: _compile_date(row, 'End time'), axis=1)
    df['duration'] = df['end'] - df['start']
    df.drop(['Date', 'Start time', 'End time'], axis=1, inplace=True)
    return df


def _clean_project_item(row, proj_dict):
    project = str(row['Project'])
    project.replace(' ', '-')
    project.replace('_', '-')
    index = project.split('-')[0]
    return proj_dict[index]


def _clean_project(df):
    # Get project set as lower case
    projects = set(df['Project'].str.lower())
    # Initialize storing dict
    proj_dict = {}
    # Loop on projects
    for project in projects:
        if str(project) == 'nan':
            proj_dict['nan'] = 'Not defined'
        else:
            # Standardized strings
            project.replace('_', '-')
            project.replace(' ', '-')
            if len(project.split('-')) == 3:
                proj_id = project.split('-')[0]
                client = project.split('-')[1].upper()
                site = project.split('-')[2].title()
                if proj_id not in proj_dict.keys():
                    proj_dict[proj_id] = f'{proj_id}-{client}-{site}'
            else:
                proj_dict[project.split('-')[0]] = project
    df['project'] = df.apply(lambda row: _clean_project_item(row, proj_dict),
                             axis=1)
    df.drop(['Project'], axis=1, inplace=True)
    return df


def _define_type(row):
    if row['project'] != 'Not defined':
        return 'client'
    else:
        return 'intern'


def _get_cat(row, act):
    try:
        return str(act[act['abbrev'] == row['Activity']].cat.values[0])
    except IndexError:
        raise ValueError('The category is invalid.')


def _get_main_cat(row, act):
    try:
        return str(act[act['abbrev'] == row['Activity']].main_cat.values[0])
    except IndexError:
        raise ValueError('The main category is invalid.')


def _split_cat(df, act):
    df['cat'] = df.apply(lambda row: _get_cat(row, act), axis=1)
    df['main_cat'] = df.apply(lambda row: _get_main_cat(row, act), axis=1)
    df.drop(['Details', 'Activity'], axis=1, inplace=True)
    return df


def _load_sheets(params):
    xl = pd.ExcelFile(pathlib.Path(params['root_folder'],
                      params['file']))
    log = xl.parse('log')
    activities = xl.parse('activities')
    holidays = list(xl.parse('official_holidays')['official_holiday'])
    paid = xl.parse('paid', index_col='date')
    return log, activities, holidays, paid


def _parse_params(par):
    par['last_check'] = datetime.datetime.strptime(par['last_check'],
                                                   '%Y-%m-%d')
    par['daily_amount'] = 3600 * par['weekly_hours'] / 5.0  # in seconds
    return par
