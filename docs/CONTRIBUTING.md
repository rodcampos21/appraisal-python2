
# Repositório destinado à matéria de *Projeto e Construção de Sistemas do CEFET/RJ* 

## Objetivo

O objetivo desse trabalho é a portabilidade do sistema appraisal para a 
línguagem python e além disso, disponibilizar um ferramental que suporte esse
sistema, ou seja, desenvolver um framework.

## O que é o Appraisal ?

O **appraisal** é um sistema para imputação de dados ausentes em conjuntos de
dados tabulares em projetos de AM(Aprendizado de Máquina) e esse sistema pode 
também gerar e validar novos valores para esses dados ausentes com base em 
diferentes abordagens.


### Regras do projeto:

Com o intuito de manter a qualidade de código, design e a organização do proje
to, foram escolhidos alguns critérios para o desenvolvimento deste projeto:

**1.** **nobrain** Utilize o [PEP8 à risca](https://pep8.org/), para tal,
  recomendo a utilização do [code formatter Black](https://github.com/psf/black).

**2.** Utilize type annotations sempre que possível.


**3.** Métodos e funções devem seguir o padrão snake case do *PEP8* e também terem
nomes descritivos. Exemplo:

  ```python

# The good
  def sum(x:float, y:float) -> float:
      """Sum two numbers"""
      return x + y

# The bad 
  def sum(x, y):
      return x + y

# The ugly 
  def sumTwoNumbers(x, y):
      return x + y

# And the evil 
  def sum_of_two_fools(x, y):
      raise Exception("An Evil Exception !!")
  ```
  **The good** - utilização de *type annotations*, com *docstring* e uma função
  descritiva.

  **The bad** - É aceitável caso seja adicionada a documentação posteriormente
  e/ou seja um "método privado" ou somente auxíliar, veja os casos de utilização,
  aqui([link1](https://stackoverflow.com/questions/1301346/what-is-the-meaning-of-single-and-double-underscore-before-an-object-name), [link2](https://en.wikipedia.org/wiki/Name_mangling#Python)).

  **The ugly** - Apenas não faça isso, siga o *PEP8*...

  **The evil** - Não crie métodos/funções *"caixa de pandora"*, onde se passa 
  algo para a função e o retorno é inesperado !!

**4.** Utilize python3.8 ou python3.9

**5.** As branchs devem ser nomeadas sempre que possível como task/<nome_da_tarefa_ou_número_da_tarefa>.
   Obs.: *Não faça commits na Master !*

**6.** Siga as tarefas da aba Projects do repositório.

**7.** Siga as *regras 5 e 6* antes de criar uma branch.

**8.** Caso não exista uma *task/tarefa*, crie na aba Projects uma com base no
   cronograma. A tarefa deve conter uma estimativa de tempo para ser completa.

    ex.: Tarefa #01
         Tempo: (0/10)

    Onde o Tempo representa o quanto de tempo foi gasto/tempo total estimado.

  Além disso, siga as *regras 5, 6 e 7*.



