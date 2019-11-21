<p align="center">
  <img src= "/Design/Logo/Logo.png"
  width="700" heigth="700"><br>
</p>


## Descrição

Com o advento de tecnologias como o WiFi e a popularização de vários sensores, bem como
o acesso à pequenos computadores (Microcontroladores embarcados) surgiu a
oportunidade de monitorar praticamente de tudo, inclusive nossos pets. Pensando nessa
ideia, surgiu o projeto de um ‘Smart Aquário’, no qual este será equipado
com vários sensores e atuadores, como sensor de temperatura [ds18b20](https://portal.vidadesilicio.com.br/sensor-de-temperatura-ds18b20/), sensor de nível de água,sensor de luminosidade,  assim como atuadores como o relé que aciona a bomba de água e o servo motor, que controla o alimentador, tudo isso utilizando uma [RaspBerry PI 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) dotado de um processador [Quad Core 1.2GHz Broadcom BCM2837](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2837/README.md). Utilizamos os serviços da [Amazon EC2](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#Home:) para criação da Máquina virtual com o sistema Linux/Ubuntu e o [Mosquitto Broker Websocket](https://mosquitto.org/) para comunicação entre nossos sensores e atuadores, com a raspberry e nosso aplicativo. O SmartAquarium será capaz de automatizar grande parte dos cuidados que devem ser tomados para manter o bem-estar dos peixes tudo isso ao controle do usuário pelo seu próprio smartphone

- [Documentação geral](/Documentação)
- [Modelo Alimentador 3D](/Protótipo/Alimentador)
- [Esquemático Raspberry Pi 3](https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3b_1p2_reduced.pdf)
- [Manual Mosquitto MQTT](https://mosquitto.org/man/mqtt-7.html)
- [Documentação de utilização Amazon EC2](https://docs.aws.amazon.com/pt_br/ec2/?id=docs_gateway)
- [Video Demonstrativo](/Video)

