#coding: utf-8
#! /usr/bin/env python
#
#Autor: Melky-Salém <msalem@globo.com>
#Descrição: 3 montes(ainda não descobri o nome) é um jogo de lógica
#			a regra é, voce deve escolher um monte e tirar quantas
#			peças quizer, desde 1 até todas, com isso em jogo até
#			dois montes vão sumir, quem pegar a ultima peça ganha
from random import randint
import sys
import time

class tresMontes(object):
	debug = False
	montes = range(3) # define montes
	qtd = [0,0,0]
	jogaPlayer1 = True # define de quem é a vez da jogada
	KAnalises = 0
	Analises = 0

	def __init__(self,qtd=[10,15,20]): # define 10,15,20 como valores iniciais ou então
		self.montes[0] = qtd[0]					# os parametros que foram passados
		self.montes[1] = qtd[1]
		self.montes[2] = qtd[2]
		self.qtd = qtd
		jogaPlayer1 = True
		if len(sys.argv) > 1:
			if sys.argv[1] == 'debug':
				debug = True

	def reseta(self):
		self.__init__(self.qtd)

	def acabou(self):
		if self.montes[0]+self.montes[1]+self.montes[2] == 0:
			return True
		return False

	def acaba(self,jogo):
		if jogo[0]+jogo[1]+jogo[2] == 0:
			return True
		return False

	def tira(self,monte,qtd):
		if self.montes[monte] >= qtd:
			self.montes[monte] -= qtd
			return True
		else:
			return False

	def imprime(self):
		if self.montes[0] > 0: print 'Monte 1:','o'*self.montes[0]
		if self.montes[1] > 0: print 'Monte 2:','o'*self.montes[1]
		if self.montes[2] > 0: print 'Monte 3:','o'*self.montes[2]

	def move_ai(self):
		atual = list(self.montes)
		if atual[0]+atual[1]+atual[2]<=10:
			nega = self.negamax(atual,1,10)
			melhor = [nega[1],nega[2]]
		else:
			if len(self.nao_vazios(atual)) == 3:
				opcoes = self.deixa_diferente(atual)
				melhor = opcoes[randint(1,len(opcoes))]
			else:
				melhor = self.deixa_igual(atual)
		self.debuga('\r'*10+'Analises: '+str(self.Analises))
		self.KAnalises = 0
		self.Analises = 0
		return melhor

	def nao_vazios(self,atual):
		nao_vazios = []
		if atual[0] > 0: nao_vazios.append(0)
		if atual[1] > 0: nao_vazios.append(1)
		if atual[2] > 0: nao_vazios.append(2)
		return nao_vazios

	def debuga(self,texto):
		if self.debug: print texto

	def deixa_diferente(self,jogo):
		opcoes = []
		for i in range(3):
			for j in range(1,jogo[i]+1):
				jogo[i] -= j
				if jogo[self.outros_dois(i)[0]] != jogo[i] and jogo[self.outros_dois(i)[1]] != jogo[i]:
					opcoes.append([i,j])
				jogo[i] += j
		return opcoes

	def deixa_igual(self,jogo):
		if jogo[self.nao_vazios(jogo)[0]] > jogo[self.nao_vazios(jogo)[1]]: return self.nao_vazios(jogo)[0],jogo[self.nao_vazios(jogo)[0]]-jogo[self.nao_vazios(jogo)[1]]
		elif jogo[self.nao_vazios(jogo)[1]] > jogo[self.nao_vazios(jogo)[0]]: return self.nao_vazios(jogo)[1],jogo[self.nao_vazios(jogo)[1]]-jogo[self.nao_vazios(jogo)[0]]
		else: return self.nao_vazios(jogo)[0],jogo[self.nao_vazios(jogo)[0]]

	def outros_dois(self,monte):
		if monte == 0: return 1,2
		if monte == 1: return 0,2
		if monte == 2: return 0,1

	def negamax(self,atual,jogador,profundidade):
		self.Analises += 1
		adversario = 1 if jogador == 2 else 1
		if self.acaba(atual) or profundidade == 0:
			self.debuga(str(profundidade)+' : acabou com pc') if jogador == 1 else self.debuga(str(profundidade)+': acabou com player')
			if jogador:
				return 1,None,None
			else:
				return -1,None,None
		else:
			value = -100
			bestValue = -100
			bestMont = -1
			bestQtd = -10
			for i in self.nao_vazios(atual):
				for j in range(1,atual[i]+1):
					atual[i] -= j
					self.debuga(str(profundidade)+' : pc') if jogador == 1 else self.debuga(str(profundidade)+' : player')
					self.debuga(str(profundidade)+' : testando monte '+str(i+1)+' quant '+str(j))
					if atual[0] > 0: self.debuga(str(profundidade)+' : Monte 1: '+'o'*atual[0])
					if atual[1] > 0: self.debuga(str(profundidade)+' : Monte 1: '+'o'*atual[1])
					if atual[2] > 0: self.debuga(str(profundidade)+' : Monte 1: '+'o'*atual[2])
					value = -self.negamax(atual,adversario,profundidade-1)[0]
					self.debuga(str(profundidade)+' : valor '+str(value))
					if value > bestValue:
						self.debuga(str(profundidade)+' : melhor agora eh '+str(value)+' '+str(i)+' '+str(j))
						bestValue = value
						bestMont = i
						bestQtd = j
					atual[i] += j
					self.debuga('\n')
			self.debuga(str(profundidade)+' : '+str(jogador)+' '+str(bestValue)+' '+str(bestMont)+' '+str(bestQtd))
			return bestValue,bestMont,bestQtd

	def inicia(self):
		print 'Jogo dos 3 Montes(Ainda não sei o nome)'
		print '*'*80
		print '**','Regra: O jogo e jogado entre duas pessoas, onde cada um deve selecionar um **'
		print '**','       monte e tirar quantas pecas quiser, quem pegar a ultima peça perde **'
		print '*'*80
		print '**','Pressione CTRL+C para sair do jogo                                         **'
		print '*'*80
		while True:
			while not self.acabou():
				self.imprime()
				if self.jogaPlayer1:
					print 'Eh a vez de PC jogar.'
					move_pc = self.move_ai()
					print 'PC do monte',move_pc[0]+1,'tirarei',move_pc[1]
					time.sleep(2)
					self.tira(move_pc[0],move_pc[1])
					self.jogaPlayer1 = False
				else:
					print 'Eh a vez de Player jogar.'
					monte = 0
					while monte not in [1,2,3] or self.montes[monte-1] <= 0:
						try:
							monte = int(raw_input('Escolha um dos Montes: '))
						except(ValueError,TypeError):
							pass
					qtd = 0
					while qtd not in range(1,self.montes[monte-1]+1):
						try:
							qtd = int(raw_input('Escolha a quantidade (entre 1 e '+str(self.montes[monte-1])+'): '))
						except(ValueError,TypeError):
							pass
					self.tira(monte-1,qtd)
					self.jogaPlayer1 = True
			vencedor = 'Player' if not self.jogaPlayer1 else 'PC'
			print vencedor,'foi o vencedor.'
			raw_input()
			self.reseta()

tresmontes = tresMontes([10,20,30])
tresmontes.inicia()