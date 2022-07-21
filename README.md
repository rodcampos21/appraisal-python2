## Objetivo

O objetivo desse trabalho é a portabilidade do sistema appraisal para a línguagem Python e além disso, disponibilizar um ferramental que suporte esse sistema, ou seja, desenvolver um framework.

## [](https://github.com/leomath42/appraisal#o-que-%C3%A9-o-appraisal-)O que é o Appraisal ?

O **appraisal** é um sistema para imputação de dados ausentes em conjuntos de dados tabulares em projetos de AM(Aprendizado de Máquina) e esse sistema pode também gerar e validar novos valores para esses dados ausentes com base em diferentes abordagens.

## Módulos

### Eraser

Módulo responsável por apagar valores de uma determinada coluna do dataset fornecido.

Sintaxe:

    python eraser.py -i <ifile> -o <ofile> -m <mech> -a <att> -r <missing_rate>

Na sintaxe acima:

- **ifile**: nome do arquivo de entrada, em formato csv.
- **ofile**: nome do arquivo de saída, em formato csv.
- **att**: nome do atributo sobre o qual simular valores ausentes.
- **mech**: mecanismo de ausência a ser aplicado. Mecanismos possíveis (todos descritos neste [documento](https://eic.cefet-rj.br/~jsoares/wp-content/uploads/2021/03/Imputac%CC%A7a%CC%83o-Hot-Deck-Uma-Revisa%CC%83o-Sistema%CC%81tica-da-Literatura-versa%CC%83o-final.pdf)) são:

  - "**MCAR**" (Missing Completely At Random)

  - "**MAR**" (Missing At Random)

  - "**NMAR**" (Not Missing At Random)

- **missing_rate**: valor entre 0 e 1, que define a taxa de valores ausentes a serem produzidos.

Um exemplo de chamada do módulo Eraser é o seguinte:

    python eraser.py -i iris.csv -o iris_missing.csv -m MCAR -a SepalLength -r .3

Em caso do mecanismo escolhido ser o NMAR, deve-se incluir um parâmetro adicional **query**, que recebe uma expressão para filtro nos valores 'x' da coluna do atributo escolhido. Tokens aceitos: x, ==, >, >=, <, <=, &, |, (,).

Um exemplo de uso para este caso é o seguinte:

    python eraser.py -i iris.csv -o iris_missing.csv -m NMAR -a "sepal.length" -r .7 -q "x >= 1 | x<=6"

### Crowner

Módulo responsável pela imputação de dados numa coluna.

Sintaxe:

    python crowner.py -i <ifile> -o <ofile> -p <plan> -a <att>

Na sintaxe acima:

- **ifile**: nome do arquivo de entrada, em formato csv.
- **ofile**: nome do arquivo de saída, em formato csv.
- **att**: nome do atributo sobre o qual preencher os valores ausentes.
- **plan**: plano de imputação a ser usado. O valor default deste argumento deve ser "mean", o que significa que os valores ausentes devem ser preenchidos com a média dos valores existentes.

Um exemplo de chamada do módulo Crowner é o seguinte:

    python crowner.py -i iris_missing.csv -o iris_filled.csv -p mean

### Reviewer

Módulo responsável pela medição de erro relativo entre os dados originais e os dados imputados.

Sintaxe:

    python reviewer.py -o <ofile> -f <ffile> -m <measure> -a <att>

Na sintaxe acima:

- **ofile**: nome do arquivo original, sem dados faltantes, em formato csv.
- **ffile**: nome do arquivo resultante da execução de um plano de imputação (usando o módulo Crowner), em formato csv.
- **att**: nome do atributo sobre o qual fazer a comparação.
- **measure**: métrica de erro a ser usada.

Um exemplo de chamada do módulo Reviewer é o seguinte:

    python reviewer.py -o iris.csv -o iris_filled.csv -m MSE -a SepalLength

### Testes Unitários

Os módulos de testes unitários estão agrupados na pasta 'Tests'.

Um exemplo de executação dos testes unitários de um módulo:

    python -m unittest Tests/test_eraser.py
