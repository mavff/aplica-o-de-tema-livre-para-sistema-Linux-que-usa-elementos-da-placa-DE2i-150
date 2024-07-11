
# Aplicação de Tema Livre para Sistema Linux Usando Elementos da Placa DE2i-150

## Descrição

Este projeto, chamado "aplicacao-de-tema-livre-para-sistema-Linux-que-usa-elementos-da-placa-DE2i-150", tem como objetivo principal o aprendizado e desenvolvimento de device drivers, a integração C/C++ com código Assembly e a compreensão do mapeamento dos periféricos da placa DE2i-150. Os periféricos incluídos neste projeto são LEDs, botões, switches e displays de 7 segmentos. Além disso, é possível a aplicação de um tema livre para sistemas Linux que utilizem os elementos da placa DE2i-150.

## Objetivos

- **Desenvolvimento de Device Drivers:** Aprender a criar e gerenciar drivers que controlam os periféricos da placa DE2i-150.
- **Integração com C/C++ com Assembly:** Implementar funcionalidades utilizando código Assembly, possibilitando um entendimento mais profundo do funcionamento do hardware.
- **Mapeamento de Periféricos:** Entender e implementar o mapeamento dos periféricos (LEDs, botões, switches e displays de 7 segmentos) da placa.
- **Aplicação Prática:** Desenvolver uma aplicação prática de tema livre para sistemas Linux utilizando os componentes da placa DE2i-150.

## Conteúdo do Projeto

- **drivers**
  - Contém os drivers desenvolvidos para os periféricos.
  
- **C**
  - Código C/c++ utilizado na integração com os drivers e para o controle direto dos periféricos.

- **application**
  - Exemplos de aplicações que utilizam os drivers e o código em C/C++ desenvolvido.
  
- **documentation**
  - Documentação detalhada sobre o desenvolvimento dos drivers, o mapeamento dos periféricos e a integração C/C++ com Assembly.

## Como Utilizar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/mavff/aplicacao-de-tema-livre-para-sistema-Linux-que-usa-elementos-da-placa-DE2i-150
   
   ```

2. **Quartus**
   - Abre o quartus 17.1(importante!) e abra o projeto pcihello.v ou aperte diretamente no arquivo.qar 
   -Mais informações sobre mapeamento estão no arquivo "[TUTORIAL] Mapeamento.pdf"
   - Se quiser adicionar o display lcd, vá no mapeamento e leia o manual da placa para dicionar corretamente.

3. **Execução das Aplicações:**
   - Compile o código e passe para a placa suas alterações, após isso, deve-se entrar no linux da placa e continuar as alterações de código lá.

