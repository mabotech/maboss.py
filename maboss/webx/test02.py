

s = "MT_T_workstation_printer"

print len(s)


v = s.split('_T_')

v2 = v[1].split('_')


y = ''.join( map(lambda x: x.capitalize() ,v2) )

print y


