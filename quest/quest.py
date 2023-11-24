print("Приветствую,игрок!")
print(
    "Вы просыпаетесь на мягкой земле, окруженные деревьями.\n"
    "Глухой лес простирается во все стороны.\n"
    "У вас нет ни карты, ни компаса, и ваша задача - выжить и выбраться из этого леса.\n"
    "Вы стоите наразвилке, перед вами два пути:\n"
    "1) Пойти налево в глубь леса.\n"
    "2) Пойти направо вдоль ручья.\n"
)
choice = int(input())
while not (1 <= choice <= 2):
    print("Такого варианта не существует. Вам дан еще один шанс.")
    choice = int(input())
if choice == 1:
    print(
        "Вы идете глубже в лес, надеясь найти выход.\n"
        "Через некоторое время вы встречаете ручей с чистой водой, но теряете направление.\n"
        "1) Найти возвышенность и осмотреть прилежащие территории.\n"
        "2) Попытаться построить примитивное укрытие.\n"
        "3) Исследовать местность вокруг.\n"
    )
    choice = int(input())
    while not (1 <= choice <= 3):
        print("Такого варианта не существует. Вам дан еще один шанс.")
        choice = int(input())
    if choice == 1:
        print(
            "Вы находите дерево, которое выглядит довольно крепким.\n"
            "Забравшись на него, видите далеко впереди светлое небо и контуры обжитой местности.\n"
            "Но ветка ломается\n"
            "под вами и вы ломаете ноги, однако ваш несломленный дух помогает вам дойти до цивилизации и выжить.\n"
        )
        win = True
    elif choice == 2:
        print(
            "Вы успешно строите укрытие, проводите ночь без происшествий, но утром осознаёте, что время потеряно.\n"
            "Вы умираете от голода и холода."
        )
        win = False
    elif choice == 3:
        print(
            "В поисках еды вы зашли на территорию волчьей стаи.\n"
            "Вас съели заживо.\n"
        )
        win = False
elif choice == 2:
    print(
        "Вы идёте вдоль ручья, который, возможно приведёт вас к какой-то населённой точке.\n"
        "Но на пути вы натыкаетесь на странный след.\n"
        "Вы следуете за следом и обнаруживаете заброшенный дом.\n"
        "1) Остаться здесь ночевать.\n"
        "2) Не оставаться и исследовать гостиную.\n"
        "3) Не оставаться и исследовать детскую комнату.\n"
    )
    choice = int(input())
    while not (1 <= choice <= 3):
        print("Такого варианта не существует. Вам дан еще один шанс.")
        choice = int(input())
    if choice == 1:
        print(
            "Не смотря на неприятный запах, вы решаете переночевать в доме.\n"
            "Решив остаться ночевать в заброшенном доме, вы не подозревали, что это была смертельная ошибка.\n"
            "Ночью вас охватила болезнь из-за вредных веществ в воздухе дома, и ваше состояние ухудшилось с каждой\n"
            "минутой.\n"
            "Несмотря на отчаянные попытки вызвать помощь, никто не услышал ваши крики о помощи.\n"
            "Вы умерли в заброшенном доме, столь же загадочно, как и это место.\n"
        )
        win = False
    elif choice == 2:
        print(
            "Вы решили не ночевать. В первую очередь вы исследуете гостиную.\n"
            "Там вы находите ружьё.\n"
            "Как только вы его взяли, дом начал рушиться, но вам удалось его покинуть.\n"
            "Вы целый день ходили по лесу, но не нашли еды, но вам повезло,\n"
            "вы находите берлогу медведя и, с помощью ружья, убиваете его, а после съедаете его.\n"
            "Однако, медведь болел бешенством.\n"
            "Вы потеряли рассудок и уже никогда не выйдете из леса.\n"
            "Этот лес станет вашим домом на остаток вашей жизни.\n"
        )
        win = False
    elif choice == 3:
        print("Вы решили не ночевать.\n"
              "В первую очередь вы исследуете детскую комнату.\n"
              "Там вы находите старый мобильный телефон.\n"
              "Как только вы его взяли, дом начал рушиться, но вам удалось его покинуть.\n"
              "Во время побега из здания вы краем глаза замечаете ружье, но не успеваете его взять.\n"
              "Взяв телефон, вы звоните по единственному доступному номеру.\n"
              "Вам отвечает мужчина и сообщает, что вы прошли квест.\n"
              "Из телефона выходит снотворный газ.\n"
              "Вы просыпаетесь у себя дома.\n"
        )
        win = True
if win == True:
    print("Поздравляем! Вы выжили.")
elif win == False:
    print("YOU DIED.")