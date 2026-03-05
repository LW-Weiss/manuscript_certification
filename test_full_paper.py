import asyncio
import ollama

# --- CONTEÚDO PARA TESTE MANUAL ---

# 1. Cole aqui a FRASE (Claim) que deu NOT_MENTIONED
CLAIM = "The entomological collection technique employed was similar to previous surveys that covered the period 2008–2010, allowing for data comparison (Kay et al., 1992a; Knox et al., 2007; Vu et al., 2012)."

# 2. Cole aqui o TEXTO COMPLETO do PDF (Copie e cole tudo, pode ser gigante)
# Dica: Use três aspas (""") para colar texto com muitas linhas
FULL_TEXT = """
NTRODUCTION
Service (1976) has reviewed a varietv of dio-
pers, weighted cone-shaped nets, and plastic and
metal cylinders with flaps used for sampling
immature mosquitoes breeding in wells. In
Myanmar (Burma), Tun-Lin et al. (1988) found
their modified netting procedure to be superior
to that recommended by the World Health Or-
ganization (1975) and reported limitations in
the latter method for well water surfaces sreater
than 3 m below ground level. The rnodified
method involved immersing a weighted net 60
cm below the well water surface and after a
minute, drawing it up through marginal debris.
In Brazil, the current method is to drop a bucket
into the well 3 times and to inspect the retrieved
water fbr immatures.
The funnel trap described herein is essentially
a simplification of earlier traps used for collect-
ing Culiseta meLanura (Coq.) from ground holes
in Maryland (Muul et aL 1974) or for Aedes
aegypti (Linn.) and Culex quinquefasciaifu.s Say
in water storage pots in Thailand (Hanison et
al. 1982). Our problem in Ceara, Brazil involved
the efficient monitoring of these 2latter species
in relation lo numbers of copepodsreleasedfor
biocontrol. Wells are common in rural villaees
and the water surface may be I0 15 m below
ground level, thus making sampling difficult.
' 'lropical Health Program, Queensland Institute of
Medical Research, Royal Brisbane Hospital P.O.,
Flrisbane, Australia 4029.
'Nricleo de Medicina Tropical, Universidade Fed-
eral do Ceara. Caixa Postal 32illl, Fortaleza, Brasil,
6 0 . 4 3 0 .
" F'undacAoNacional da Saude, Ministerio de Saude,
Fortaleza, CearA, Brasil, 60,000.
''Tropical Health Program, University of Queens-
land Medical School, Herston, Brisbane, Australia
4006.
MATERIALS AND METHODS
Funnel trap design: The trap functioned on 2
premises: 1) immature mosquitoes and copepods
were guided by the inverted funnel into the
reservoir when they swam toward the surface,
and 2) trapping of air in the reservoir ensured
that the device floated unaided. It comprised 4
parts: 1) a 22 cm diam. plastic funnel, 2) a 500
ml polystyrene jar (reservoir) with screw cap
(Corning cat. no. 25628-500),3) a 50 g sinker,
and 4) cord for attachment with a length, de-
pending on the depth ofthe wells (Fig. 1). Spare
reservoirs and caps were useful for taking the
catch back to the laboratory. When the reser-
voirs were removed, the funnels (plus cord and
sinker) stacked conveniently on top of each
other.
The trap was assembled by cutting out the
middle of the screw cap along the inside of the
concentric groove and glueing this ring onto the
funnel spout approximately 5-6 cm below its tip.
The cord was knotted before and after threadins
through a hole at the rim of the funnel, leaving
10 cm spare for sinker attachment. Double knot-
ting prevented the sinker from pulling the at-
tachment cord taut so that the trap could float
unhindered, and loss of the trap if the sinker
became detached.
To operate, the jar was filled with 400 ml
clean water which when inverted left a 3-4 cm
air pocket for flotation. The jar was then
screwed onto the funnel and the trap lowered,
reservoir-up, into the well. On immersion, the
weight of the sinker inverted the trap into its
collecting mode. For retrieval, the trap was in-
verted by pulling the cord, coming out of the
well funnel-up.
Eualuation of the trap: Trap efficiency was
compared by day and by night within the Federal
University of CearA grounds in a 1,000 liter
Mesocyclops aspericornis (Daday) mass culture
tank and in 1.5 x 1 x 0.3 m sections of an
FuNNu, TRnp l'on SeruPt,tN<;WnllsD E C E M B E R1 9 9 2
Q z z c m D
F i s . l . T h e t u n n e l t r a p : f r o m t o p ; r e s e r v o i r , f u n n e l
zrnd sinker.
effluent treatment pond containing Cx. quinque-
fasciatus.Over six 24-h periods, one and 2 traps'for M. aspericornis and Cr. quinquefasciatus,
respectively, were used over the hours of 1830-
0715 and 0730-1800. Contents of each reservoir
were emptied into white trays for counting and
then returned to their respective sites. Although
the traps were moved to different positions
within each site, the integrity of the paired day
vs night comparisons was preserved. Log (x +
1) counts were then compared by Student's f-
test.
To determine if immature Cx' quinquefascia'
tus were escaping from the reservoir through the
2 cm diameter funnel tip, 150-200 third-fourth
instar larvae were put in the reservoir and those
remaining were counted after 10 hours. This was
repeated with a reduced nozzle diameter of 1 cm
with both Cx. quinquefasciatus and M. asperi-
cornis.
The suburb of Granja Portugal in Fortaleza
was chosen for survey because of its numerous
wells. From February to April 1992, 285 wells
were surveyed for immature mosquitoes, fish
and copepods by trapping from approximately
1700 to 0800 h. Surface area, well depth and
water volume were also recorded. In order to
determine the sensitivity and efficacy of the
f'unnel traps, the following numbers (and num-
ber of replicates) of mixed third-fourth instar
Cx. quinquefasciatus were introduced into nega-
tive wells: 10 (8), 25 (12),50 (8), 100 (9)' 200
( 8 ) , 4 0 0 ( 6 ) , 6 0 0 ( 4 ) , 1 0 0 0 ( 3 ) , 1 5 0 0 ( 6 ) a n d 2 0 0 0
(4). From 0800 to 1700 h prior to each of these
68 releases,traps were left in the wells to recheck
their negativity.
On the next day the following numbers (and
number of replicates) of Mesocyclops aspericor-
nis were released into the wells: 25 (4)' 50 (4)'
1 0 0 ( 4 ) , 2 0 0 ( 4 ) , 4 0 0 ( 4 ) , 5 0 0 ( 2 ) a n d 8 0 0 ( 4 ) . A s
before, the traps were run from 1700 to 0800 h
and the nu-Ee. recovered counted in white
trays. The numbers recovered in the traps were
then analysed in relation to numbers released
using SPSS statistics software.
RESULTS
Time of trapping: During night and day, re-
spectively, the following totals were collected:
Cx. quinquefasciatus larvae 501 and 299, pupae
61 and 24; M. aspericornis 3,860 and 3'066.
When log (x + 1) catches were compared by t-
test, there were no significant difTerenceseither
f o r C x . q u i n q u e f a s c i a t u s( t : 1 . 1 8 , d f : 1 1 , P :
0.26) or for M. aspericornis(t: 0.34, df : 5, P
: 0 . 7 5 ) .
Escape from the trap: After 6 x 12 h trapping
periods, from 12.1 to 29.3% of Cx. quinquefatgm-
,us larvae had swum out of the reservoir. With
a reduced opening of 1 cm diameter, losses were
still of the same order. During 3 overnight trials
with the 1 cm diameter nozzle and M' aspericor-
nis,8-12% had escapedfrom the reservoir by
the next morning.
Sensitiuity: The surface area of the funnel in
comparison with that of the wells was 3.8% ' The
overall averagerecovery for Cx. quinquefasciatus
and M. aspericornis, respectively, was 6.1 and
3.6%. For Cx. quinquefasciatus,percent recovery
tended to decrease with increasing population
size. The sensitivity of the overnight funnel
traps for detecting presence of Culex larvae or
MesocycLopswas dependent on the number of
animals released. Detection success reached
IO0o/ofor 100 or more larvae (Table 1) or 400 or
more copepods (Table 2). The lowest sensitivity
noted was 50o/oof traps positive for 10 larvae or
for 25 copepods. At this level of infestation,
repeated trappings would increase the eventual
sensitivity of detection to the following levels:
75.87.94 and 97% successfor the second,third,
fburth and fifth nights, respectively.
Prediction: Pearson's correlation coefficients
of r : 0.84 and 0.73 for copepods and larvae,
respectively, indicated that the proportion re-
covered was relatively constant across a range
of population levels (Tables l and 2). From this,
r' values suggested that 7I% and 53% of varia-
tion in the numbers captured were explained by
variation in the numbeis of copepods and larvae
released.However, on the basis of one trap night
per well, interpolation of catch size to the size
of the natural population would be imprecise'
Thus, regression equations to predict popula-
tions on ihe basis of the number captured have
not been included.
Suruey of wells: For 285 wells in Granja Por-
tugal, tlie mean surface area * SD (range) and
mean distance from the well rim to the water
JounNer,oF THE AueRrceu Mosquno CoNrnor, Assoclerron V o L . 8 , N o . 4
Table 1. Mean recovery of Culex quinquefasciatus larvae from funnel traps placed overnight in wells, in
relation to number of larvae released.
Recovery
No. released No. trials
Mean no.
+ S D Range %
Sensitivity
(?i, positive)
7 . 7
6.9
o ^
4.8
6 . 7
4.6
2 . 4
4 . r
0 - l
'I'able 2. Mean recovery of MesocycLopsaspericornis from funnel traps placed overnight in wells, in relation to
number of copepods released.
Recovery
1i)
50
100
200
400
600
1,000
1,500
2,000
Totals
0.8 -r 1.0
1 . 9+ 1 . 6
1 . 6+ 1 . 7
6.9 -f 1.5
18.9r- 8.2
19.2+ 8.0
4 0 . 3+ 1 2 . 1
46.3+ 9.3
35.1+ I2.4
81.5+ 75.0
0-:l
0 5
0-4
6-9
1r-36
9-32
23-50
36-54
74-47
30 193
50
83
O J
100
100
100
100
100
100
100
87
8
1 2
8
9
8
6
4
3
6
4
68
No. released No. trials
M e a n n o .
+ S D Range %
Sensitivity
(% positive)
9 R
50
100
200
400
500
800
Totals
0.5 -|-0.6
2 . 5+ 3 . 1
3 . 8+ 2 . 9
3 . 0+ 3 . 8
20.5 + 19.2
17.5t- 7.8
35.5+ 7.0
0-1
0-7
0-6
0 8
o * o
12-23
3 1 - 4 6
4
2
4
2 6
50
75
50
00
00
00
7 7
2.0
5.0
3 . 8
1 . 5
o . l
3.5
4.4
. 1 . O
Ievelr- SD (range)was 1.1+ 0.35m, (0.7- 4.8
m') and 1.5 + 1.1 m (0 to 6.3 m). Well volume
rangedfrom 4,400to 11,600liters. No wellswere
positive for Ae. aegypti;27wercpositive for Cx.
quinquefasciatus,35 for cyclopid copepodsin-
cluding Mesocyclopsspp. and b9 for fish. The
total number of larvae and pupaecollected,re-
spectively,was 9,902and 1,055.In one heavilv
infestedwell, the funnel trap contained>b,00b
larvae and >500 pupae after one night's trap-
ping. After eliminating this extremecatch from
calculations,the mean numbers of larvae and
pupae recoveredfrom the funnel traps were
188.5and 17.5,respectively.
DISCUSSION
Apart from the evaluatibnsat GranjaPortugal
where water levelswere high and free of debris,
we have also usedthe funnel traps successfully
in wells at Vila Manuel Satiro and at Preaoca
where the water surface was 8-10 m below
ground level and sometimeslittered with float-
ing coconutsand wood.We havecollectedmos-
quito immatures,copepods,ostracods,fish and
tadpoles.
After approximately 350 trap nights, Ae. ae-
gyptihas yet to be collected from wells in Ceara.
However, approximately I0% contained Cr.
quinquefasciatiusimmatures and in some cases
in enormous numbers. Harrison et al. (1982)
considered their AFRIMS (Armed Forces Re-
search Institute of Medical Sciences) trap to be
more efficient for collectin g Cx. quinquefasciatus
than Ae. aegypti because of their comparative
feeding habits. Our trap would have similar
characteristics to the AFRIMS trap but contains
less parts. With one sinker, the inverted funnel
lies in the water approximately 5" off the hori-
zontal, but this is inconsequential. A second
sinker can be added if desired but cost is a maior
considerationwhen working in developingcoun-
tries. This model costs US $4 and can be used
in water depths over 40 cm. This design could
be produced in different sizes (and with different
and less expensive materials) to accommodate
mosquito and copepod biotopes of different sizes
and depths. The important developmental con-
siderations are the trapping of air within the
reservoir and the balance achieved between the
sinker and reservoir of water to make the tran
invert on immersion.
Although efficiency seemed similar for day
and night, trapping by night was more practical
|)ECEMBER 1992 F u N N s r , T R A P l o R S e u p t , t N c W E L L S 375
as the water surfacewas less likely to be dis-
turbed through water retrieval for domestic
usage.Consequently,trap damagewas reduced.
Trap returns of Cx. quinquefasciatusand M.
aspericornisaveraged6.1and 3.6%,respectively,
but on the basisof a singlenight, the variability
in returns precludedpreciseestimationof pop-
ulation size. Although 53% of the variability
with the returns of Cx. quinquefasciatuswas
explainedby population size, catchescould be
influencedthe position of the trap (i.e.,against
the side or in the middle) and by clustering of
the larval population itself. We are not con-
vinced that the apparenttendencyfor reduced
percent recovery of Cx. quinquefasciatuswith
increasedpopulation size is real although the
clustereddistribution may changewhen the pop-
ulation is large.
As the modesof respirationof mosquitolarvae
and copepodsare different,we would expectthe
funnel traps to be more sensitive for detecting
the former. For C.x.quinquefasciatus larv ae,50Vo
werepositiveat 1 larva/1,000cm2(10 per well)
and all werepositiveat 1/100cm' (100per well).
As Mesocyclopsaspericornisoccupiesall of the
water column but primarily is benthic (Brown
and Kay, unpublisheddata),the detectionof 25
in a well containing a minimum of 4,400liters
of water is particularly pleasing(1/176 liters).
Sensitivity was a key issue with respect to
developmentof thesefunnel traps for sampling
from wells. Currently, all wells are treated with
temephosgranulesat 1 g/liter aspart of national
health policy. For the 285 wells surveyed at
Granja Portugal,this implies usageof approxi-
mately 2,000 kg per treatment. If policy is al-
tered to treat only the 27 wells found positive
then lessthan 200kg would be required.Should
greater precisionbe required as a policy base,
then trapping over4 consecutivenights per neg-
ative well yields 95% confidenceof lessthan 10
larvae/well.On the basis of laboratory evalua-
tion (Kay et al. 1992),we intend to monitor the
efficacyand persistenceof predaciouscyclopids,
especiallyM. longisetus(Thi6baud)releasedfor
biocontrolof Cx.quinquefasciatusin comparison
with the existing copepodand fish populations
found during our survey.
"""

# --- CONFIGURAÇÃO ---
OLLAMA_MODEL = "llama3.1"

async def teste_manual():
    print(f"📄 Tamanho do texto: {len(FULL_TEXT)} caracteres.")
    print("🧠 Lendo e verificando (isso pode demorar um pouco mais que o abstract)...")
    
    start = asyncio.get_running_loop().time()
    
    prompt = f"""You are a scientific fact-checker.
    CLAIM: "{CLAIM}"
    SOURCE TEXT: "{FULL_TEXT}"
    
    Does the SOURCE TEXT support the CLAIM?
    
    Reply STRICTLY in this format:
    VEREDITO: [SUPPORTIVE / CONTRADICTORY / NOT_MENTIONED]
    EXPLICAÇÃO: [Short explanation in Portuguese]
    """

    # Chamada direta
    try:
        response = await asyncio.to_thread(
            ollama.chat, 
            model=OLLAMA_MODEL, 
            messages=[{'role': 'user', 'content': prompt}]
        )
        output = response['message']['content']
    except Exception as e:
        output = f"Erro: {e}"
        
    end = asyncio.get_running_loop().time()
    
    print("\n" + "="*40)
    print(output)
    print("="*40)
    print(f"⏱️ Tempo total: {end - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(teste_manual())