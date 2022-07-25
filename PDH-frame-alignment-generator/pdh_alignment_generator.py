#!/usr/bin/env python3.8

import random
import time

# X0011011 FAS
# X1AXXXXX NFAS

# Vemos el timeslot 0 y queremos lograr la alineación de trama

# Suposición, cuando se prende el equipo B, el equipo A
# Siempre empieza a escuchar desde la FAS de B0




def channel_noise(trama,max_bits_affected):

    # To remove problems with memory allocation
    trama = list(trama)
    
    # To decide if the 'trama' is going to be affected or not by the channel noise
    
    if random.choice([0,1]) == 1:

        # To fix how many bits can be affected by the channel channel noise

        if 0 > max_bits_affected or max_bits_affected > 8:
            max_bits_affected = 8  
         

        # Initialize vector and counter
        index_of_affected_bits = []
        i=0

        # To affect the number of bits that I want to modify
        while i < max_bits_affected:

            # To choose random index
            index_affected = random.randint(0,7)

            # If the selected index has not modified yet
            if index_affected not in index_of_affected_bits:
                
                # Append that index to the list
                index_of_affected_bits.append(index_affected)

                # If the value of that index is zero or one
                if trama[index_affected] == '0' or trama[index_affected] == '1':

                    # Put a random 0 or 1 in that place
                    trama[index_affected] = str(random.choice([0,1]))
                else:
                    # If is an X, put an X
                     trama[index_affected] = 'X'
                
                # Increment the counter 
                i+=1

    # Return noise-affected 'trama'
    return trama



# TxB + Noise = RxA


# 'Start' indicates in what fas-'trama' number start to transmit B equipment (start = 1)
def communication(start, max_bits_affected):


    fas=['X','0','0','1', '1', '0', '1', '1']
    nfas=['X','1','0','X', 'X', 'X', 'X', 'X']
    nfas_a=['X','1','1','X', 'X', 'X', 'X', 'X']
    false_vector= [False,False,False,False,False,False,False,False]


    tramas_tx_A =[] # Are not affected by channel noise
    tramas_rx_A = [] # Affected by channel noise


    # To complete the initial states befort B starts to transmit
    for i in range(1,start*2+1):
        
        if (i%2) != 0:

            # if is an odd number of 'trama'
            tramas_tx_A.append(fas)
            tramas_rx_A.append(false_vector)
        else:

            # if it is an even number of 'trama'
            tramas_tx_A.append(nfas_a)
            tramas_rx_A.append(false_vector)


    alignment = False
    alignment_counter =[]
    
    # While the alignment has not completed yet
    while alignment == False:

        # Receive fas-'trama' (with noise)
        trama_rx_fas = channel_noise(fas, max_bits_affected)

        # Save tx and rx 'trama'
        tramas_tx_A.append(fas)
        tramas_rx_A.append(trama_rx_fas)
       
        if trama_rx_fas == fas:
            
            # If fas-'trama' is OK, then count a 'fas' step
            alignment_counter.append('fas')

            # Then, receive a nfas-'trama'
            trama_rx_nfas = channel_noise(nfas_a, max_bits_affected)
            tramas_rx_A.append(trama_rx_nfas)
            
            # Check alignment
            if alignment_counter != ["fas","nfas","fas"]:

                # If is not aligned, save a nfas with alarm
                tramas_tx_A.append(nfas_a)

                if trama_rx_nfas[1] == nfas[1]:

                    # If it's OK, then count a 'nfas' step and save a tx trama without alarm.
                    alignment_counter.append('nfas')

                else:
                    # If is not OK, then reset the alignment counter  
                    alignment_counter= []

            else:
                
                # If it's OK, save nfas without alarm and set alignment=True
                tramas_tx_A.append(nfas)
                alignment = True

        else:

            # Reset alignment counter
            alignment_counter= []

            # Only save a new rx nfas 'trama'
            trama_rx_nfas = channel_noise(nfas_a, max_bits_affected)
            tramas_rx_A.append(trama_rx_nfas)
            
            # And transmit a nfas_a 
            tramas_tx_A.append(nfas_a)
                

    
    return tramas_tx_A, tramas_rx_A






# To enter the information

bits_affected = int(input("Ingrese la cantidad de bits que quiere afectar (de 0 a 8):\n"))
start = int(input("Ingrese en qué trama FAS quiere empezar la recepción (>=0):\n"))

# To control execution time
t_start = time.time()

# Generating a tx and rx vectors. rx starts in the 2nd fas-'trama' and have 7 bits affected by channel noise.
tx_and_rx = communication(start,bits_affected)


print("\n")
print("Alineación de trama:\n")

print("TX\t\t\t\t\t\tRX\n")


# To count alignment time
total_time = 0


for k in range(len(tx_and_rx[0])):
    
    # To remove 'False' elements at the printing moment
    if tx_and_rx[1][k][0] != False:

        # To count time of alignment
        total_time +=125

        
        # print tx and rx
        if (len(tx_and_rx[0])-1) > k > (len(tx_and_rx[0])-5):
            
            print(str(tx_and_rx[0][k])+"\t"+ str(tx_and_rx[1][k])+"*")
        else:
            if k == (len(tx_and_rx[0])-1):
                print(str(tx_and_rx[0][k])+"*"+"\t"+ str(tx_and_rx[1][k]))
            else:
                print(str(tx_and_rx[0][k])+"\t"+ str(tx_and_rx[1][k]))

    else:
        # print tx
        print(str(tx_and_rx[0][k])+"\t")


print("\n")



print(f'Tramas recibidas para lograr alineación: {int((total_time-125)/125)} [tramas]')
print(f'Tiempo para lograr alineación: {total_time-125} [us]')

# To control execution time

t_end = time.time()

print(f'Tiempo de ejecución: {round((t_end-t_start)*1E6,2)} [us]')



