import random
import time
q=0.01
while q<10:
    print ('New')
    hum = random.randint(1,6)
    ai = random.randint(1,6)
    q=q+0.01
    ais=0
    hums=0
    if hum>ai:
        print ('Win')
        print ('you '+ str (hum))
        print ('It '+ str (ai))
        hums=hums + hum +1
        ais=ais + ai 
    elif hum<ai:
        print ('Lose')
        print ('you '+ str (hum))
        print ('It '+ str (ai))
        hums=hums + hum
        ais=ais + ai +1
    else:
        print ('Tie')
        print ('you '+ str (hum))
        print ('It '+ str (ai))
        ais=ais + ai
        hums=hums + hum
print('You got '+ str(hums) +' points')
print('It got '+ str(ais) +' points')

    
    


