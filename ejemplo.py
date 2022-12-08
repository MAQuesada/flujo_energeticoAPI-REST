from datetime import datetime, timedelta

d = datetime.today()

f = d.replace(year=2019)
# print(f, '++++++\n', f >= d, type(f-d))

year = 2010
for mes in range(1, 13):

    print('mes ', mes)
    fech_inicio = datetime(year=year, month=mes, day=1)

    if mes == 12:
        fech_fin = datetime(year=year, month=(2), day=1)
        fech_fin = fech_fin - timedelta(days=1)
        fech_fin = fech_fin.replace(month=mes)
    else:
        fech_fin = datetime(year=year, month=(mes+1), day=1)
        fech_fin = fech_fin - timedelta(days=1)

    print(fech_inicio, '------>', fech_fin, fech_inicio <= fech_fin)

x = (datetime.strptime('2020-04-19 12:00:00', '%Y-%m-%d %H:%M:%S'))

x = x - timedelta(days=1)
