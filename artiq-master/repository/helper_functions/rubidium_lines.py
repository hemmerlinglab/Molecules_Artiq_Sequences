import numpy as np

def create_transition(atom, gs, es, Fg, Fe, Fe_co = '', crossover = False):

    if not crossover:
        freq = atom[gs + '-' + es] + atom[gs][str(Fg)] + atom[es][str(Fe)]
        label = atom['atom'] + ' ' + Fg + '->' + Fe
        ls = '-'
    else:
        freq = atom[gs + '-' + es] + atom[gs][str(Fg)] + (atom[es][str(Fe)] + atom[es][str(Fe_co)])/2.0
        label = atom['atom'] + ' ' + Fg + '->' + Fe + '/' + Fe_co + ' (co)'
        ls = '--'

    return [freq, label, ls]



def calculate_Rb_transitions():

    Rb87 = {
            'atom' : 'Rb87',
            'S1/2-P3/2' : 384.230484468e12,
            'S1/2-P1/2' : 377.107463380e12,
            'S1/2' : {
                '2' : -2.563005979e9,
                '1' : 4.271676631e9
                },
            'P3/2' : {
                '3' : +193.7407e6,
                '2' : -72.9112e6,
                '1' : -229.8518e6,
                '0' : -302.0738e6
                },
            'P1/2' : {
                '2' : +305.44e6,
                '1' : -509.06e6,
                }
            }
    
    Rb85 = {
            'atom' : 'Rb85',
            'S1/2-P3/2' : 384.230406373e12,
            'S1/2-P1/2' : 377.107385690e12,
            'S1/2' : {
                '3' : -1.264888516e9,
                '2' : 1.770843922e9
                },
            'P3/2' : {
                '4' : +100.205e6,
                '3' : -20.435e6,
                '2' : -83.835e6,
                '1' : -113.208e6
                },
            'P1/2' : {
                '3' : +150.659e6,
                '2' : -210.923e6,
                }

        }
   
 
    # only keeping the lines that cycle photons
   
    # P3/2
    #my_lines = []
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P3/2', '2', '3'))
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P3/2', '2', '2', Fe_co = '3', crossover = True))
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P3/2', '2', '1', Fe_co = '3', crossover = True))
    #
    #my_lines.append(create_transition(Rb85, 'S1/2', 'P3/2', '3', '4'))
    #my_lines.append(create_transition(Rb85, 'S1/2', 'P3/2', '3', '3', Fe_co = '4', crossover = True))
    #my_lines.append(create_transition(Rb85, 'S1/2', 'P3/2', '3', '2', Fe_co = '4', crossover = True))
    
    # P1/2
    my_lines = []
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P1/2', '1', '2'))
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P1/2', '1', '1', Fe_co = '2', crossover = True))
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P1/2', '1', '1'))

    #my_lines.append(create_transition(Rb87, 'S1/2', 'P1/2', '2', '2'))
    #my_lines.append(create_transition(Rb87, 'S1/2', 'P1/2', '2', '1', Fe_co = '2', crossover = True))
    
    #my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '2', '2'))
    my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '2', '3'))
    my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '2', '2', Fe_co = '3', crossover = True))

    my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '3', '2'))
    my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '3', '3'))
    my_lines.append(create_transition(Rb85, 'S1/2', 'P1/2', '3', '2', Fe_co = '3', crossover = True))
   
    return my_lines


def get_rb_scan_interval(no_of_points = 5, df = 50.0, cnt_freq = 384.230e12):

    # creates intervals over hyperfine lines of Rb transitions
    scan_interval = []
    
    lines = calculate_Rb_transitions()

    cnt = []
    for k in range(len(lines)):
        cnt.append(np.float(lines[k][0]) - cnt_freq)

    cnt = np.sort(np.array(cnt))

    df = df * 1e6
    
    for k in range(len(lines)):
        hlp = np.linspace(cnt[k] - df, cnt[k] + df, no_of_points)
        scan_interval.extend(hlp)

    scan_interval = np.array(scan_interval)/1e6

    return scan_interval


