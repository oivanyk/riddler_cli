import numpy as np
from sentence_transformers import SentenceTransformer
import random
import time
import os

SIM_THRESHOLD = 0.92

random.seed(time.time())

def cos_similarity(vector_a, vector_b):
    # Compute dot product
    dot_product = np.dot(vector_a, vector_b)

    # Compute L2 norms (magnitudes)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    
    # Compute cosine similarity

    norm = norm_a * norm_b
    if(norm==0):
        norm+=1e-8

    cosine_sim = dot_product / norm

    return cosine_sim

def delete_dublic_matrix(matrix, column):
    unic_fields = set()
    result = []

    for row in matrix:
        field = row[column]
        if field not in unic_fields:
            unic_fields.add(field)
            result.append(row)
    
    return result
    
def yes_or_no(word):
    if(word =="y" or word =="yes" or word =="tak" or word =="t"):
        return 1
    elif(word =="n" or word =="no" or word =="nie"):
        return 0
    else:
        return -1
        
def draw_bar(seta, set):
    if(seta>set or seta<0 or set<0):
        print()
        return
    seta = int(seta)
    set = int(set)
    if(set<=0):
        coef= 0
    else:
        coef = int(100/set)
    
    print()
    print('|'+ seta*coef*'▉' + (100-seta*coef)*' ' + '|')
    print()
    
#---model load---
model = SentenceTransformer("./models/minilm")

#----Data Load----
zz_text = np.load(r'baza_zagadek/zbiorzagadekT.npy')
zz_emb = np.load(r'baza_zagadek/zbiorzagadekE.npy')
z72_text = np.load(r'baza_zagadek/66zagadekT.npy')
z72_emb = np.load(r'baza_zagadek/66zagadekE.npy')

base_text = np.concatenate((zz_text, z72_text), axis=0)
base_emb = np.concatenate((zz_emb, z72_emb), axis=0)

dic_text = np.load("slownik/slownikT.npy")
dic_emb = np.load("slownik/slownikE.npy")




#Funkcja odpowiada za rozwiązywanie zagadek:
#Znajduje najbardziej podobne słowa ze słownika oraz najbardziej podobne zagadki z bazy zagadek
def solver():
    rid = input("Wpisz zagadkę: ")
    rid = rid.strip()
    rid = rid.lower()
    rid_emb = model.encode(rid)
    results = [None]*len(base_emb)
    word_results = [None]*len(dic_text)
    for i in range(len(base_emb)):
        results[i] = [base_text[i][0], cos_similarity(rid_emb, base_emb[i][1])]
    for i in range(len(dic_text)):
        word_results[i] = [dic_text[i], cos_similarity(dic_emb[i], rid_emb)]
    
    results.sort(key=lambda x: x[1], reverse=True)
    word_results.sort(key=lambda x: x[1], reverse=True)

    results = delete_dublic_matrix(results, 0)

    prev_res_print_lim = 0
    res_print_lim = 5

    prev_wres_print_lim = 0
    wres_print_lim = 5
    solver_active = 1

    while(solver_active==1):

        print("Wyniki z bazy zagadek: ")
        for i in range(prev_res_print_lim, res_print_lim):
            print(results[i][0], results[i][1])

        print("\nWyniki ze słownika: ")
        for i in range(prev_wres_print_lim, wres_print_lim):
            print(word_results[i][0], word_results[i][1])
        
        print()
        next_results = input("Czy chcesz wyświetlić kolejne 10 wyników? (tak/nie): ")
        next_results = next_results.strip()
        next_results = next_results.lower()
        if(next_results=="y" or next_results=="yes" or next_results=="tak" or next_results=="t"):
            prev_res_print_lim = res_print_lim
            prev_wres_print_lim = wres_print_lim
            res_print_lim+=5
            wres_print_lim+=5
        elif(next_results=="n" or next_results=="no" or next_results=="nie"):
            solver_active=0
        else:
            print("Podano niepoprawny ciąg znaków\n")

def finder():
    print("\nProgram spróbuje znaleźć zagadkę do podanego słowa")
    word = input("Wpisz słowo: ")
    word = word.strip()
    word = word.lower()
    word_emb = model.encode(word)
    results = [None]*len(base_emb)

    print()

    for i in range(len(base_text)):
        results[i] = [base_text[i][1], base_text[i][0], cos_similarity(word_emb, base_emb[i][0]), i+1]

    results.sort(key=lambda x: x[2], reverse=True)
    results = delete_dublic_matrix(results, 0)


    prev_res_print_lim = 0
    res_print_lim = 3
    finder_active = 1

    while(finder_active==1):
        for i in range(prev_res_print_lim, res_print_lim):
            print(f"Zagadka nr{results[i][3]}")
            print(results[i][0], "(", results[i][1], ")", "Podobieństwo: ", results[i][2]*100, "%\n" )
        
        print()
        next_results = input("Czy chcesz wyświetlić kolejne 3 zagadki? (tak/nie): ")
        next_results = next_results.strip()
        next_results = next_results.lower()

        print()
        if(next_results=="y" or next_results=="yes" or next_results=="tak" or next_results=="t"):
            prev_res_print_lim = res_print_lim
            res_print_lim+=3
        elif(next_results=="n" or next_results=="no" or next_results=="nie"):
            finder_active=0
        else:
            print("Podano niepoprawny ciąg znaków\n")

def if_riddle_has_multiple_answers(uanswer, answers):
    max_sim = -1
    answers_emb = model.encode(answers)
    uanswer_emb = model.encode(uanswer)

    cosim = cos_similarity(answers_emb, uanswer_emb)
    if(cosim > max_sim):
        max_sim = cosim

    answers = answers.split(",")
    if("," in uanswer):
        uanswer = uanswer.split(",")
        uanswer_emb = model.encode(uanswer)
    else:
        uanswer_emb = [uanswer_emb]

    answers_emb = model.encode(answers)

    for i in answers_emb:
        for j in uanswer_emb:
            cs = cos_similarity(i, j)
            if(cs > max_sim):
                max_sim = cs
    return max_sim

def one_game(riddle_index=None):

    if riddle_index is not None:
        riddle_id = riddle_index
    else:
        riddle_id = random.randint(0, len(base_text)-1)

    print()
    print(base_text[riddle_id][1])
    print()

    score = 0
    

    answer = input("Twoja odpowiedź: ")
    answer = answer.strip()
    answer = answer.lower()
    answer_emb = model.encode(answer)

    if("," in base_text[riddle_id][0]):
        cosim = if_riddle_has_multiple_answers(answer, base_text[riddle_id][0])
    else:   
        cosim = cos_similarity(answer_emb, base_emb[riddle_id][0])
        
    print(f"Podobieństwo: {round(cosim*100)}%")
    if(cosim>=SIM_THRESHOLD):
        print("Poprawna odpowiedź to:", base_text[riddle_id][0])
        print(" ✔ ( +5 pkt)")
        score=5
        return score
    print("\nTwoja odpowiedź nie jest poprawna. Możesz spróbować jeszcze 2 razy\n")

    answer = input("Twoja odpowiedź: ")
    answer = answer.strip()
    answer = answer.lower()
    answer_emb = model.encode(answer)

    if("," in base_text[riddle_id][0]):
        cosim = if_riddle_has_multiple_answers(answer, base_text[riddle_id][0])
    else:   
        cosim = cos_similarity(answer_emb, base_emb[riddle_id][0])

    print(f"Podobieństwo: {round(cosim*100)}%")
    if(cosim>=SIM_THRESHOLD):
        print("Poprawna odpowiedź to:", base_text[riddle_id][0])
        print(" ✔ ( +3 pkt)")
        score=3
        return score
    print("\nTwoja odpowiedź nie jest poprawna. Możesz spróbować jeszcze raz\n")

    answer = input("Twoja odpowiedź: ")
    answer = answer.strip()
    answer = answer.lower()
    answer_emb = model.encode(answer)

    if("," in base_text[riddle_id][0]):
        cosim = if_riddle_has_multiple_answers(answer, base_text[riddle_id][0])
    else:   
        cosim = cos_similarity(answer_emb, base_emb[riddle_id][0])

    print(f"Podobieństwo: {round(cosim*100)}%")

    if(cosim>=SIM_THRESHOLD):
        print("Poprawna odpowiedź to:", base_text[riddle_id][0])
        print(" ✔ ( +1 pkt)")
        score=1
        return score
    else:
        print(" ✘ ( -1 pkt)")
        print("Poprawna odpowiedź to:", base_text[riddle_id][0])
        return -1


def game():

    user_data_file = "user_data/user_data.npy"
    user_names_file = "user_data/user_names.npy"


    # User data validation and load
    if not os.path.exists(user_data_file) or not os.path.exists(user_names_file):
        
        def_user_data = [[0,0,0,0]]
        def_user_names = ["user"]
        np.save(user_names_file, def_user_names)
        np.save(user_data_file, def_user_data)


    user_data = np.load(user_data_file)
    user_names = np.load(user_names_file)


    user_chosen = 0
    while(user_chosen == 0):

        username = input("Podaj nazwę użytkownika: ")
        username = username.strip()
        username = username.lower()


        if not np.isin(username, user_names):
            add_user = input("Użytkownik o podanej nazwie nie istnieje. Czy chcesz dodać nowego użytkownika? (tak/nie): ")
            add_user = add_user.strip()
            add_user = yes_or_no(add_user)

            if(add_user == 1):
                user_names = np.append(user_names, username)
                user_data = np.vstack((user_data, [0,0,0,0]))
                user_chosen=1
                user_id = len(user_names) - 1
            elif(add_user == 0):
                print()
            else:
                print("Podano niepoprawny ciąg znaków\n")
        else:
            user_chosen = 1
            user_id = np.where(user_names == username)[0][0]
            
    np.save(user_names_file, user_names)
    np.save(user_data_file, user_data)

    game = 1
    while(game==1):

        print(f"\nWitaj, {user_names[user_id]}!\n")
        print("Wybierz tryb gry: \n\tJedna zagadka (wpisz 1) \n\tRunda z 5 zagadek (wpisz 2) \n\tZobacz statystykę (wpisz 3)\n\nAby wyjść z trybu gry wpisz 0 lub exit")
        game_mode = input()
        game_mode = game_mode.strip()
        game_mode = game_mode.lower()

        if(game_mode=="1"):
            score = one_game()
            if(score>0):
                user_data[user_id][0]+=1
                user_data[user_id][3]+=score
            else:
                user_data[user_id][1]+=1
                user_data[user_id][3]+=score

            np.save(user_data_file, user_data)

        elif(game_mode=="2"):
            overall_score = 0
            win_count = 0
            for i in range(5):
                score = one_game()
                overall_score+=score
                user_data[user_id][3]+=score
                if(score>0):
                    win_count+=1
                    user_data[user_id][0]+=1
                else:
                    user_data[user_id][1]+=1

                np.save(user_data_file, user_data)
            if(win_count==1):
                print("Odgadłeś 1 zagadkę z 5.")
            elif(win_count==5):
                print("Odgadłeś wszystkie zagadki!")
            else:
                print(f"Odgadłeś {win_count} zagadki z 5.")
            
            if(overall_score > user_data[user_id][2]):
                print(f"Końcowy wynik: {overall_score} (NOWY REKORD!)")
                print(f"Wcześniejszy maksymalny wynik końcowy to: {user_data[user_id][2]}")
                user_data[user_id][2]=overall_score
                np.save(user_data_file, user_data)
            else:
                print(f"Końcowy wynik: {overall_score}")
            
            print()


        elif(game_mode=="3"):
            print(f"\nStatystyka użytkownika \"{user_names[user_id]}\" :")
            print("\nLiczba gier:", user_data[user_id][0] + user_data[user_id][1])
            print(f"Liczba rozwiązanych zagadek: {user_data[user_id][0]}")
            print(f"Liczba nierozwiązanych zagadek: {user_data[user_id][1]}")
            draw_bar(user_data[user_id][0], user_data[user_id][0] + user_data[user_id][1])
            if(user_data[user_id][0] + user_data[user_id][1] <=0):
                win_percent = 50
            else:
                win_percent = round((user_data[user_id][0] / (user_data[user_id][0] + user_data[user_id][1]))*100, 2)
            print(f"Rozwiązujesz poprawnie {win_percent}% zagadek")
            print(f"Maksymalny wynik w rundzie: {user_data[user_id][2]}")
            print(f"Liczba punktów: {user_data[user_id][3]}")

        elif(game_mode=="0" or game_mode=="exit"):
            game=0
            print("Wyjście z gry")
        
        elif(game_mode == "choose_by_index"):
            riddle_input = input(f"Podaj numer zagadki [1 - {len(base_text)}]: ")
            if(riddle_input.isnumeric() and int(riddle_input) in range(1, len(base_text)+1)):
                score = one_game(riddle_index=int(riddle_input)-1)
            else:
                print("Podano niepoprawny ciąg znaków\n")
            
        else:
            print("Podano niepoprawny ciąg znaków\n")


active_main=1
while(active_main==1):
    print("\n")
    print("Witaj w Riddler. To program do odgadywania i wyszukiwania zagadek. \nWybierz tryb: \n\tTryb rozwiązywania zagadek (wpisz 1) \n\tTryb wyszukiwania zagadek (wpisz 2) \n\tTryb gry (wpisz 3)\n\nAby wyjść z programu wpisz 0 lub exit")
    
    mode = input()
    mode = mode.strip()
    mode = mode.lower()
    if(mode=="1"):
        solver()
    elif(mode=="2"):
        finder()
    elif(mode=="3"):
        game()
    elif(mode=="0" or mode=="exit"):
        active_main=0
        print("Wyjście z programu")
    else:
        print("Podano niepoprawny ciąg znaków\n")

