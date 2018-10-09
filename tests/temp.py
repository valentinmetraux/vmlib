import vmlib

@vmlib.timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

waste_some_time(1)

a = vmlib.survey.points.Survey_point(site="site", line=111, point_type='rcv', point_id="caca", note='A loooooooooooooooog note')




print(a)

a
