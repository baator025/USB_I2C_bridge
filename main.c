#include <avr/io.h>
#include <stdlib.h>
#include "uart.h"
#include "i2c.h"


int main(void){
	uart_init(9600);
	i2c_init();
	
	uint8_t address;
	uint8_t *data;
	uint8_t flag;
	uint8_t size;
	uint8_t i;
	
    while (1){
		flag = receive_frame();							//receive info about work mode
		send_frame(flag);
		
		//write mode, in this case, atmega will resend data from uart to i2c. 
		if(flag == 'w'){								//write mode condition 
			address = get_frame();						//receive i2c destination address
			size = get_frame();							//get size of work data 
			
			data = malloc(size);						//allocate buffer with work data
			if(data == NULL){							
				send_frame('e');
			}
			
			for(i=0; i<size; i++){						//receive data and write to buffer
				*(data + i) = get_frame();
			}
			i2c_send_chunk(address, size, data);		//send data from buffer on i2c bus
			free(data);
			data = NULL;
		}
		
		//scan mode, in this case atmega will sweep through all addresses and capture the one, which sends ack
		if(flag == 's'){								//scan mode condition
			address = i2c_scan();						//scan 
			send_frame(address);						//return address via uart
		}
    }
}