import copy
import unidecode
import streamlit as st

frequents = []
firsts = []
text_file = open("wordle.txt", "r")
str = text_file.read().split(",")

if 'tryable_words' not in st.session_state:
    st.session_state.tryable_words = copy.deepcopy(str)
#tryable_words = str
ok_letters = ["_", "_", "_", "_", "_"]
nok_letters = []
containing = []
misplaces = [[], [], [], [], []]
# print(len(str))
test = []

if 'nb_lettre' not in st.session_state:
    st.session_state.nb_lettre = 5
if 'type_de_jeu' not in st.session_state:
    st.session_state.type_de_jeu = "Wordle"
if 'type_de_jeu_old' not in st.session_state:
    st.session_state.type_de_jeu_old = "Wordle"

def init_variables():
    #print("INIT VARIABLES")
    if (st.session_state.nb_lettre!=5) :
        i=0
        global ok_letters
        ok_letters= []
        global misplaces
        misplaces= []
        while (i<st.session_state.nb_lettre):
            ok_letters.append("_")
            misplaces.append([])
            i+=1
    #print(ok_letters)
    #print(misplaces)

def load_file():
    #print("LOAD FILE - Type : ", st.session_state.type_de_jeu)
    if (st.session_state.type_de_jeu == "Sutom"):
        text_file = open("sutom.txt", "r")
        str = text_file.read().split(",")
        str = [unidecode.unidecode(word) for word in str if len(word) == st.session_state.nb_lettre]
        #print(str)

    if (st.session_state.type_de_jeu == "Wordle"):
        text_file = open("wordle.txt", "r")
        str = text_file.read().split(",")

    st.session_state.tryable_words = copy.deepcopy(str)

def read_input(texte):
    length = 0
    index = 0
    t = list(texte)
    while length < len(texte):
        c = t[length]
        if (c == '+'):
            ok_letters[index] = t[length + 1]
        if (c == '-'):
            nok_letters.append(t[length + 1])
        if (c == '*'):
            misplaces[index].append(t[length + 1])
        if (c == '#'):
            containing.append(t[length + 1])
        length += 2
        index += 1
    #print(ok_letters)
    #print(nok_letters)
    #print(misplaces)


def filter_words():
    #init_variables()
    misplaces_flat = []
    for tmp in misplaces:
        for tmp2 in tmp:
            misplaces_flat.append(tmp2)

    for mot in st.session_state.tryable_words:
        add_word = True
        array_index = 0
        # print('—------------------------------------------------')
        # print(tryable_words[array_index])
        # print(mot)
        lettres = list(mot.lower())
        index = 0
        for c in nok_letters:
            if c in mot.lower():
                add_word = False
                break
        for c in containing:
            if c not in mot.lower():
                add_word = False
                break
        for m in misplaces_flat:
            if m not in mot.lower():
                add_word = False
                break
        while index < st.session_state.nb_lettre:
            l = lettres[index]
            ok = ok_letters[index]
            misplace = misplaces[index]
            # print('mot : ',mot,' and index : ',index,' and l : ',l,' and ok :', ok)
            if ok != '_' and l != ok:
                add_word = False
                break
            if len(misplace) > 0:
                for x in misplace:
                    if l == x:
                        add_word = False
                        break
            index += 1
        if add_word:
            test.append(mot)


def freq(texte):
    d = {}
    for c in texte:
        if c.lower() not in d:
            if c not in car:
                d[c.lower()] = 1
        else:
            d[c.lower()] += 1

    return d


def first(texte):
    d = {}
    for c in str:
        if c.lower()[0] not in d:
            d[c.lower()[0]] = 1
        else:
            d[c.lower()[0]] += 1

    return d

st.set_page_config(
     page_title="Wordle Solver",
     #page_icon="🧊",
     #layout="wide",
     #initial_sidebar_state="expanded",
     #menu_items={
     #    'Get Help': 'https://www.extremelycoolapp.com/help',
     #    'Report a bug': "https://www.extremelycoolapp.com/bug",
     #    'About': "# This is a header. This is an *extremely* cool app!"
     #}
 )

st.title("Wordle Finder")
st.header("Resolveur de Wordle")
st.subheader("Instructions :")
st.text("- Les lettres bien placées sont précédée de +")
st.text("- Les lettres mal placées sont précédée de *")
st.text("- Les lettres absentes sont précédée de -")
st.text("- Les lettres présentes sont précédée de #")
#trys = 0
#while True:
#    print("Essai n° ", trys+1)
#    result = input('Enter result: ')
#    if(result=='stop'):
#        break
#    read_input(result)
#    filter_words()
#    print(test)
    # print(len(tryable_words))
    # print(len(str))
#    trys += 1
#    tryable_words = copy.deepcopy(test)
#    test = []

st.session_state.type_de_jeu = st.radio(
     "Quel type de jeu",
     ('Wordle', 'Sutom'))

if st.session_state.type_de_jeu == 'Wordle' and st.session_state.type_de_jeu_old == 'Sutom':
    load_file()
    st.session_state.type_de_jeu_old = 'Wordle'

#print(st.session_state.type_de_jeu,"/",st.session_state.type_de_jeu_old)

if st.session_state.type_de_jeu == 'Sutom':
    lettres = st.text_input("Nombre de lettres", key=2)
    if(lettres!=""):
        st.session_state.nb_lettre = int(lettres)
        init_variables()
        if st.session_state.type_de_jeu_old == 'Wordle':
            load_file()
            st.session_state.type_de_jeu_old = 'Sutom'

result = st.text_input("Enter result", key=1)
reinit = st.button("Reinit list")
if(reinit):
       #st.session_state.tryable_words = copy.deepcopy(str)
    load_file()


read_input(result)
filter_words()

st.write(len(st.session_state.tryable_words))
st.markdown(test)
#tryable_words = copy.deepcopy(test)
st.session_state.tryable_words = copy.deepcopy(test)
test = []

