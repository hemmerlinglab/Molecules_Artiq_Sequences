import numpy as np

#####################################################################

def get_atom_data(atom = 'Rb85'):

    # dictionary of atoms
    # down to hyperfine
    # data[atom]

    # All frequencies in Hz
    # All hyperfine splitting frequencies are relative to the fine structure
    
    atom_data = {
            'Rb87' : {
                'S1/2-P3/2' : 384.230484468e12,
                'S1/2-P1/2' : 377.107463380e12,
                'S1/2' : {
                    2 : -2.563005979e9,
                    1 : +4.271676631e9
                    },
                'P3/2' : {
                    3 : +193.7407e6,
                    2 : -72.9112e6,
                    1 : -229.8518e6,
                    0 : -302.0738e6
                    },
                'P1/2' : {
                    2 : +305.44e6,
                    1 : -509.06e6,
                    }
                },
            'Rb85' : {
                'S1/2-P3/2' : 384.230406373e12,
                'S1/2-P1/2' : 377.107385690e12,
                'S1/2' : {
                    3 : -1.264888516e9,
                    2 : +1.770843922e9
                    },
                'P3/2' : {
                    4 : +100.205e6,
                    3 : -20.435e6,
                    2 : -83.835e6,
                    1 : -113.208e6
                    },
                'P1/2' : {
                    3 : +150.659e6,
                    2 : -210.923e6,
                    }
                }
            }

    return atom_data[atom] 


#####################################################################

def get_transition_freq(atom, Ji, Jf, Fi, Ff):

    # calculates the absolute transition frequency of specific atom from |Ji, Fi> -> |Jf, Ff>
    d = get_atom_data(atom)

    electronic_transition = '{0}-{1}'.format(Ji, Jf)

    # fine structure transition
    freq_fine_structure = d[electronic_transition]

    # hyperfine splitting
    freq_HFS_i = d[Ji][Fi]
    freq_HFS_f = d[Jf][Ff]

    # add fine structure and hyperfine splitting
    freq_abs = freq_fine_structure + freq_HFS_i + freq_HFS_f

    return freq_abs


#####################################################################

def get_Rb_transitions():

    atom = 'Rb87'

    Ji = 'S1/2'
    Jf = 'P3/2'

    freqs_arr = [
            get_transition_freq(atom, Ji, Jf, 2, 3),
            get_transition_freq(atom, Ji, Jf, 2, 2),
            ]

    # add cross-over transitions
    freqs_arr.extend([
             (freqs_arr[0]+freqs_arr[1])/2.0,     
           ])

    atom = 'Rb85'

    Ji = 'S1/2'
    Jf = 'P3/2'

    freqs_arr.extend([get_transition_freq(atom, Ji, Jf, 3, 4)])
    freqs_arr.extend([get_transition_freq(atom, Ji, Jf, 3, 3)])

   

    vs = np.sort(freqs_arr)

    aom = 85e6

    for v in vs:
        print('{0:.6f}'.format( (v + aom) / 1e12 ))


    return 



