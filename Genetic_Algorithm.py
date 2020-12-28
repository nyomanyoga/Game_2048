import random
import csv

def gen(ax):
	temp=[]
	for x in range(ax*15):
		temp.append(random.randint(0,1))
	return temp

def populasi (besar):
	populasi=[];ax=0
	for x in range(besar):
		ax=random.randint(1,10)
		populasi.append(gen(ax))
	return populasi

def hitungFit(urutan, data_latih):
	fit=[];
	for x in range(len(urutan)):
		a=len(urutan[x])/15;avg=[];b=0;p=0
		while(b<a and urutan[x][(b*15)+14]==1):
			cek=0
			for y in range(15):
				if(urutan[x][(b*15)+y]==1):
					cek+=1
			if(cek!=15):
				total=0
				for j in range(len(data_latih)):
					status='false';status1='false';status2='false';status3='false'
					for i in range(3):
						if(urutan[x][(b*15)+i]==data_latih[j][i]==1):
							status='true'
					for i in range(3,7):
						if(urutan[x][(b*15)+i]==data_latih[j][i]==1):
							status1='true'
					for i in range(7,11):
						if(urutan[x][(b*15)+i]==data_latih[j][i]==1):
							status2='true'
					for i in range(11,14):
						if(urutan[x][(b*15)+i]==data_latih[j][i]==1):
							status3='true'
					if(status==status1==status2==status3=='true' and data_latih[j][14]==1):
						total+=1;
					elif(data_latih[j][14]==0):
						total+=1;
				avg.append(total/len(data_latih))
			b+=1
		if(avg!=[]):
			for o in range(len(avg)):
				p+=avg[o]
			fit.append(p/len(avg))
		else:
			fit.append(0)
	return fit

def proba(fit):
	z=[];y=0
	for x in range(len(fit)):
		y+=fit[x]
	if(y==0):
		z.append(0)
	else:
		for x in range(len(fit)):
			z.append(fit[x]/y)
	return z

def check(Probabilitas,i):
	if(Probabilitas[i]<=0.15):
		b=1
	elif(Probabilitas[i]>0.15 and Probabilitas[i]<=0.25):
		b=2
	elif(Probabilitas[i]>0.25 and Probabilitas[i]<=0.35):
		b=3
	elif(Probabilitas[i]>0.35 and Probabilitas[i]<=0.45):
		b=4
	elif(Probabilitas[i]>0.45 and Probabilitas[i]<=0.55):
		b=5
	elif(Probabilitas[i]>0.55 and Probabilitas[i]<=0.65):
		b=6
	elif(Probabilitas[i]>0.65 and Probabilitas[i]<=0.75):
		b=7
	elif(Probabilitas[i]>0.75 and Probabilitas[i]<=0.85):
		b=8
	elif(Probabilitas[i]>0.85 and Probabilitas[i]<=0.95):
		b=9
	elif(Probabilitas[i]>0.95):
		b=10
	return b

def pemilihanprob(Probabilitas):
	ran=[];y=0
	for i in range(len(Probabilitas)):
		for j in range(check(Probabilitas,i)):
			ran.append(Probabilitas[i])
	return ran

def randomFitness(ran, Probabilitas):
	rand=[]
	for x in range(len(Probabilitas)):
		rand.append(random.choice(ran))
	return rand

def search(terpilih,Probabilitas):
	indeks=[]
	for x in range(len(Probabilitas)):
		for i in range(len(Probabilitas)):
			if terpilih[x]==Probabilitas[i]:
				indeks.append(i)
				break
	return indeks

def idks(indeks,parent):
	aa=[]
	for x in range(len(indeks)):
		temp=[]
		for i in range(len(parent[indeks[x]])):
			temp.append(parent[indeks[x]][i])
		aa.append(temp)
	return aa

def crossOver(win):
	for x in range(int(len(win)/2)):
		temp=[];temp1=[]
		t1=random.randint(0,len(win[2*x])-2)
		t2=random.randint(1,len(win[2*x])-1)
		if(t1!=len(win[2*x])-2):
			while(t2<=t1):
				t2=random.randint(1,len(win[2*x])-1)
		else:
			t2=len(win[2*x])-1
		a=(t2-t1)%15
		tk1=random.randint(0,(len(win[2*x+1])-1)-a)
		tk2=tk1+a
		temp=win[2*x][t1:t2+1]
		del win[2*x][t1:t2+1]
		temp1=win[2*x+1][tk1:tk2+1]
		del win[2*x+1][tk1:tk2+1]
		z=len(temp1)-1
		while(z>=0):
			win[2*x].insert(t1,temp1[z])
			z-=1
		y=len(temp)-1
		while(y>=0):
			win[2*x+1].insert(tk1,temp[y])
			y-=1
	return win

def mutasi(parent):
	anak=crossOver(parent)
	p=0
	for p in range(len(anak)):
		for i in range(len(anak[p])):
			if(random.uniform(0,1)<0.01):
				if(anak[p][i]==1):
					anak[p][i]=0
				else:
					anak[p][i]=1
	return anak

#Seleksi Pemilihan Orang Tua Baru
def pemilihanPbaru(parent,anak, FitP, FitC):
	fixL=[];fixFit=[];o=0;p=0
	for q in range(len(FitP)):
		buf=parent[q-o];bufFit=FitP[q-o]
		for i in range(len(FitC)):
			if(bufFit<FitC[i]):
				buf=anak[i]
				bufFit=FitC[i]
		fixL.append(buf);fixFit.append(bufFit)
		if(bufFit==FitP[q-o]):
			parent.pop(q-o);FitP.pop(q-o)
			o+=1
		else:
			ax=0
			while(bufFit!=FitC[ax]):
				ax+=1
			anak.pop(ax);FitC.pop(ax)
			p+=1
	return fixL+fixFit

#Mencari Indeks Kromosom Terbaik
def cekTerbaik(fitness):
	idk=0
	sem=fitness[0]
	for x in range(1,len(fitness)):
		if(sem<fitness[x]):
			sem=fitness[x]
			idk=x
	return idk

def bacaData():
	f = open('data_latih.csv', 'r')
	reader = csv.reader(f)
	a=[];b=[];c=[];d=[];e=[]
	for row in reader:
	    a.append(row[0])
	    b.append(row[1])
	    c.append(row[2])
	    d.append(row[3])
	    e.append(row[4])
	latih=[]
	for i in range(len(a)):
		#parameter tinggi, normal, rendah
		suhu = []
		if(a[i]=='tinggi'):
			suhu=[1,0,0]
		elif(a[i]=='normal'):
			suhu=[0,1,0]
		else:
			suhu=[0,0,1]
		#parameter pagi, siang, sore, malam
		waktu=[]
		if(b[i]=='pagi'):
			waktu=[1,0,0,0]
		elif(b[i]=='siang'):
			waktu=[0,1,0,0]
		elif(b[i]=='sore'):
			waktu=[0,0,1,0]
		else:
			waktu=[0,0,0,1]
		#parameter cerah, berawan, rintik, hujan
		cuaca=[]
		if(c[i]=='cerah'):
			cuaca=[1,0,0,0]
		elif(c[i]=='berawan'):
			cuaca=[0,1,0,0]
		elif(c[i]=='rintik'):
			cuaca=[0,0,1,0]
		else:
			cuaca=[0,0,0,1]
		#parameter tinggi, normal, rendah
		kelembaban = []
		if(d[i]=='tinggi'):
			kelembaban=[1,0,0]
		elif(d[i]=='normal'):
			kelembaban=[0,1,0]
		else:
			kelembaban=[0,0,1]
		#parameter ya,tidak
		terbang = []
		if(e[i]=='ya'):
			terbang=[1]
		else:
			terbang=[0]
		latih.append(suhu+waktu+cuaca+kelembaban+terbang)
	f.close()
	return latih

def bacaDataUji():
	f = open('data_uji.csv', 'r')
	reader = csv.reader(f)
	a=[];b=[];c=[];d=[];e=[]
	for row in reader:
	    a.append(row[0])
	    b.append(row[1])
	    c.append(row[2])
	    d.append(row[3])
	uji=[]
	for i in range(len(a)):
		#parameter tinggi, normal, rendah
		suhu = []
		if(a[i]=='Tinggi'):
			suhu=[1,0,0]
		elif(a[i]=='Normal'):
			suhu=[0,1,0]
		else:
			suhu=[0,0,1]
		#parameter pagi, siang, sore, malam
		waktu=[]
		if(b[i]=='Pagi'):
			waktu=[1,0,0,0]
		elif(b[i]=='Siang'):
			waktu=[0,1,0,0]
		elif(b[i]=='Sore'):
			waktu=[0,0,1,0]
		else:
			waktu=[0,0,0,1]
		#parameter cerah, berawan, rintik, hujan
		cuaca=[]
		if(c[i]=='Cerah'):
			cuaca=[1,0,0,0]
		elif(c[i]=='Berawan'):
			cuaca=[0,1,0,0]
		elif(c[i]=='Rintik'):
			cuaca=[0,0,1,0]
		else:
			cuaca=[0,0,0,1]
		#parameter tinggi, normal, rendah
		kelembaban = []
		if(d[i]=='Tinggi'):
			kelembaban=[1,0,0]
		elif(d[i]=='Normal'):
			kelembaban=[0,1,0]
		else:
			kelembaban=[0,0,1]
		uji.append(suhu+waktu+cuaca+kelembaban)
	f.close()
	return uji

def jawabDataUji(listT, data_uji):
	terbang=[]
	for x in range(len(data_uji)):
		c=0;kebenaran=False
		while(c<len(listT)/15 and (not kebenaran) and listT[(c*15)+14]==1):
			cek=0
			for y in range(15):
				if(listT[(c*15)+y]==1):
					cek+=1
			if(cek!=15):
				status='false';status1='false';status2='false';status3='false'
				for i in range(3):
					if(data_uji[x][i]==listT[(c*15)+i]):
						status='true'
				for i in range(3,7):
					if(data_uji[x][i]==listT[(c*15)+i]):
						status1='true'
				for i in range(7,11):
					if(data_uji[x][i]==listT[(c*15)+i]):
						status2='true'
				for i in range(11,14):
					if(data_uji[x][i]==listT[(c*15)+i]):
						status3='true'
				if(status==status1==status2==status3=='true'):
					kebenaran=True
			c+=1
		if(kebenaran):
			terbang.append(1)
		else:
			terbang.append(0)
	return terbang

def tulisJawaban(jawaban):
	f = open('hasil.csv', 'w')
	w = csv.writer(f)
	w.writerow(jawaban)
	f.close()

#Main Program Genetic Algorithm
print("\t\t\t\t --- Genetic Algorithm ---")
besar=(int(input('Masukan besar populasi : ')))
parent=populasi(besar)
a=0
fitBuffer=[]
while(a<25):
	fitness=hitungFit(parent, bacaData())
	Probabilitas = proba(fitness)
	ran=pemilihanprob(Probabilitas)
	terpilih = randomFitness(ran, Probabilitas)
	indeks=search(terpilih,Probabilitas)
	win=idks(indeks,parent)
	anak=mutasi(win)
	fitness2=hitungFit(anak, bacaData())
	baru = pemilihanPbaru(parent,anak,fitness,fitness2)
	parent=baru[0:int(len(baru)/2)]
	if(fitBuffer==[]):
		fitBuffer=baru[int(len(baru)/2):len(baru)]
	else:
		if(fitBuffer==baru[int(len(baru)/2):len(baru)]):
			a+=1
		else:
			fitBuffer=baru[int(len(baru)/2):len(baru)]
			a=0
listTerbaik=baru[0:int(len(baru)/2)][cekTerbaik(baru[int(len(baru)/2):len(baru)])]
print('Rule :',listTerbaik, '\n')
jawaban=jawabDataUji(listTerbaik, bacaDataUji())
print('Hasil Data Uji :',jawaban)
tulisJawaban(jawaban)
print('\t\tJawaban Berhasil Disimpan Pada hasil.csv ')