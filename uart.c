#include <avr/io.h>

void uart_init(volatile uint16_t speed){
	UCSR0B |= (1<<RXEN0);							//enabling uart pins
	UCSR0B |= (1<<TXEN0);
	//frame format
	UCSR0B &= ~(1<<UCSZ02);							//8-bit frame
	UCSR0C |= ((1<<UCSZ01)|(1<<UCSZ00));
	UCSR0C &= ~((1<<UMSEL00)|(1<<UMSEL01));			//asynchronous mode
	UCSR0C &= ~((1<<UPM00)|(1<<UPM01));				//no parity bit
	UCSR0C &= ~(1<<USBS0);							//1 stop bit
	//data rate
	UCSR0A &= ~(1<<U2X0);							//divider on
	unsigned int ubrr= 0;
	ubrr=(((F_CPU / (speed * 16UL))) - 1);			//speed calculation
	UBRR0H = (unsigned char) (ubrr>>8);
	UBRR0L = (unsigned char) ubrr;
}

void send_frame(uint8_t data){
	while ( !( UCSR0A & (1<<UDRE0)) );
	UDR0 = data;
	//while ( !( UCSR0A & (1<<UDRE0)) );
}

uint8_t receive_frame(void){
	while ( !(UCSR0A & (1<<RXC0)) );
	return UDR0;
}

uint8_t get_frame(void){
	while(1){
		if((UCSR0A&(1<<RXC0)) == (1<<RXC0)){
			break;
		}
	}
	while ( !(UCSR0A & (1<<RXC0)) );
	return UDR0;
}