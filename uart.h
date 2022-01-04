void uart_init(volatile uint16_t speed);
void send_frame(uint8_t data);
uint8_t receive_frame(void);
uint8_t get_frame(void);