import random

# ARQUIVO .TSP TRANFORMADO EM MATRIZ .TXT
arquivo = open("test-cases/caso5(AG).txt", "r")
matriz = []
linha = arquivo.readline()
while linha != "":
    elementos = linha.split()
    matriz.append(elementos)
    linha = arquivo.readline()

arquivo.close()

# PEGAR CORDENADAS E COLOCAR EM DICIONARIO
cordenadas = []
dicio_pontos = {}
for i in range(len(matriz)):
    for j in range(len(matriz[0])):
        letra = matriz[i][j]
        if matriz[i][j] == 'R':
            dicio_pontos[letra] = (i, j)
        elif matriz[i][j] != '0':
            dicio_pontos[letra] = (i, j)
            cordenadas.append(letra)
cordenadas = sorted(cordenadas)


#ALGORITMO GENÉTICO
def algoritmoGenetico(cordenadas, tamanhoPopulacao, taxaDeReproducao, probabilidadeMutacao, criterioParada):
    # PREENCHENDO POPULAÇÃO A PARTIR DO TAMANHO DA ENTRADA
    populacao = []
    cont = 0
    while cont < tamanhoPopulacao:
        pt =  cordenadas * 1
        individuo = []
        for i in range(len(cordenadas)):
            id = random.randint(0, len(pt) - 1) #RECEBE ID ALEATORIO
            individuo.append(pt[id])
            pt.remove(pt[id]) #REMOVE PARA NÃO REPETIR
        populacao.append(individuo)
        cont += 1
        
    # ORDENANDO POR APTIDÃO
    populacao = sorted(aptidao(populacao))

    # CALCULANDO APTIDÃO DAS GERAÇÕES
    for k in range(ciclomaximo):
      
      for i in range(tamanhoPopulacao):
        print("Geração: {} | {}".format(k, populacao[i])) #PRIMEIRA
        
      aptidaoTotal = 0 # soma das aptidoes de todos individuos
      for i in range(0, tamanhoPopulacao):
        aptidaoTotal = aptidaoTotal + populacao[i][0]

 
      # PESO DE CADA INDIVIDUO PARA ROLETA 
      piso = 0
      for i in range(tamanhoPopulacao):
        populacao[i].append(round(aptidaoTotal/populacao[i][0], 2)) #AREDONDA PESO E ADICIONA AO INDIVIDUO  
        populacao[i].append(round(piso + populacao[i][2], 2))
        piso = round(piso + populacao[i][2] + 0.01, 2)

      # RETORNANDO OS PARES DE PAIS PARA CROSSOVER
      pais = roleta(populacao, taxaDeReproducao)
      novaPopulacao = crossover(pais, probabilidadeMutacao)
      populacao = sorted(populacao + novaPopulacao)
      """ 
      3 * 2 = 6
      10 + 6 = 16 
      """
      # AJUSTE POPULACIONAL
      populacao = ajustePopulacional(populacao, tamanhoPopulacao)

      # PRINTANDO POPULAÇÕES

      

    return populacao


# CALCULO DA APTIDÃO
def aptidao(populacao):
    aptidaoPop = []
    for i in range(len(populacao)):
        aptidaoIndivi = []
        soma_distancia = 0
        

        """ 
        Aptidaopopulação = [[100, ['a', 'b', 'c']], [100, ['a', 'b', 'c']], [100, ['a', 'b', 'c']]]
        """
        
        pt = str(populacao[i][0])#ELEMENTO E CORDENADA
        soma_distania = soma_distancia + dist_pontos(dicio_pontos['R'][0], dicio_pontos['R'][1], dicio_pontos[pt][0], dicio_pontos[pt][1])
        
        #GERA OS INDIVIDUOS DA POPULAÇÃO 
        for j in range(len(populacao[i])):
            if j == len(populacao[i]) - 1:
                pt = str(populacao[i][j])
                soma_distania = soma_distancia + dist_pontos(dicio_pontos[pt][0], dicio_pontos[pt][1], dicio_pontos['R'][0],
                                                    dicio_pontos['R'][1])
            else:
                ptA = str(populacao[i][j])
                ptB = str(populacao[i][j + 1] )
                soma_distancia = soma_distancia + dist_pontos(dicio_pontos[ptA][0], dicio_pontos[ptA][1], dicio_pontos[ptB][0],
                                                    dicio_pontos[ptB][1])

        #ADICIONA O INDIIDOS E SUA DISTANCIA COMO UM MEMBRO DA POPULAÇÃO 
        aptidaoIndivi.append(soma_distancia)
        aptidaoIndivi.append(populacao[i])
        aptidaoPop.append(aptidaoIndivi)

    return aptidaoPop


# CALCULO DA DISTANCIA GEOMETRICA DA MATRIZ
def dist_pontos(x1, y1, x2, y2):
    D = abs((x2-x1))+abs((y2-y1))
    return D


# METÓDO DA ROLETA
def roleta(populacao, taxaDeReproducao):
    pop = populacao[:]
    cont = 0
    pais = []
    taxa = int(len(populacao) * ((taxaDeReproducao/2) / 100)) # Como são pares de pais 100% é o mesmo que a metade dos individuos
    
    while cont < taxa:
        pai = []
        for i in range(0, 2):
            limite = round(pop[int(len(pop)/2)][3], 2) 
            ponteiro = round(random.uniform(pop[0][3]-1, limite), 2)
            for j in range(len(pop)-1):
                if j == 0:
                    limiteInferior = 0
                    limiteSuperior = pop[j][3] 
                    if ponteiro > limiteInferior and ponteiro <= limiteSuperior:
                        pai.append(pop[j])
                        pop.remove(pop[j])
                        break
                else:
                    limiteInferior = pop[(j-1)][3]
                    limiteSuperior = pop[j][3]
                    if ponteiro > limiteInferior and ponteiro <= limiteSuperior:
                        pai.append(pop[j])
                        pop.remove(pop[j])
                        break
        pais.append(pai)
        cont += 1

    return pais


# CROSSOVER
def crossover(pais, probabilidaDeMutacao):
    novaPopulacao = []
    pontoCorte = random.randint(1, len(pais[0][0][1])-1)
    for i in range(0, len(pais)-1):
        pai1 = pais[i][0][1]
        pai2 = pais[i][1][1]
        
        """ 

          pai1: [1, 2, 3, 4]
          pai2: [2, 3, 4, 1]
          filho: [3, 2, 4, 1]
        """
        
        filho1 = pai1[0:pontoCorte]+pai2[pontoCorte:len(pai2)]
        filho2 = pai2[0:pontoCorte]+pai1[pontoCorte:len(pai1)]
        filho1 = mutacao(filho1, probabilidaDeMutacao)
        filho2 = mutacao(filho2, probabilidaDeMutacao)
        orgarnizarFilho(pai1, filho1)
        orgarnizarFilho(pai1, filho2)
        novaPopulacao.append(filho1)
        novaPopulacao.append(filho2)
    novaPopulacao = sorted(aptidao(novaPopulacao))

    return novaPopulacao


# MUTAÇÃO
def mutacao(filho, taxaDeMutacao):
    taxa = random.uniform(0.0, 1.0)
    if taxa < taxaDeMutacao:
        id = random.randint(0, len(filho)-1)
        id2 = random.randint(0, len(filho)-1)
        filho[id], filho[id2] = filho[id2], filho[id]
    
    return filho


# REMOVENDO REPETIÇÕES DE LETRAS
def orgarnizarFilho(pai, filho):
    # verificando as letras repetidas e as letras faltando
    letrasRepetidas = [k for k in pai if filho.count(k) > 1]
    letraFaltando = list(set(pai).difference(set(filho)))
    ids = []

    # Verificando os indices das letras repetidas
    if letrasRepetidas == []:
        return filho
    else:
        for i in range(0, len(letrasRepetidas)):
            c = 0
            for x in range(0, len(filho)):
                if filho[x] == letrasRepetidas[i]:
                    c += 1  # contador para não pegar o primeiro item da lista
                    if c > 1:
                        ids.append(x)

    for j in range(0, len(ids)):
        filho[ids[j]] = letraFaltando[j]
    return filho


# AJUSTE POPULACIONAL
def ajustePopulacional(populacao, tamanhoPopulacao):
  """ Com elitismo sem convergencia"""
  while len(populacao) > tamanhoPopulacao:
    tam = len(populacao)
    individuo1 = random.randint(0, tam-1)
    individuo2 = random.randint(0, tam-1)
    if individuo1 != individuo2:
      if populacao[individuo1][0] < populacao[individuo2][0]:
          populacao.remove(populacao[individuo2])
      else:
          populacao.remove(populacao[individuo1])
  
  return populacao


tamanhoPopulacao = 10
taxaDeReproducao = 60
probabilidadeMutacao = 0.5
ciclomaximo = 80


# IMPRIMINDO MELHOR RESULTADO
ag = algoritmoGenetico(cordenadas, tamanhoPopulacao, taxaDeReproducao, probabilidadeMutacao, ciclomaximo)
print("Melhor solução encontrada: {} | {}".format(ag[0][0], ag[0][1]))
