import csv
import pygame

SIZE = HEIGHT, WIDTH = 1280, 720
FPS = 60
font = 'data/Fonts/Font1.ttf'
font_size = 30
health_bar_width, energy_bar_width = 20, 20
health_bar_height, energy_bar_height = 200, 150


def import_csv(link):
    with open(link, encoding='utf-8') as file:
        spisok = csv.reader(file, delimiter=',')
        spisok = [i for i in spisok]
        return spisok


player_stats = {'health': 100, 'speed': 4, 'energy': 75, 'exp': 0}

pict_items = {
    'трава': ['data/grass/grass_1.png',
              'data/grass/grass_2.png',
              'data/grass/grass_3.png',
              'data/grass/grass_4.png',
              'data/grass/grass_5.png',
              'data/grass/grass_6.png',
              'data/grass/grass_7.png',
              'data/grass/grass_8.png'
              ]

}

slovar_layouts_level1 = {
    'границы': import_csv('data/level_graphics/lvl1_layouts/borders.csv'),
    'трава': import_csv('data/level_graphics/lvl1_layouts/grass.csv'),
    'монстры': import_csv('data/level_graphics/lvl1_layouts/monsters.csv'),
    'переходы': import_csv('data/level_graphics/lvl1_layouts/transitions.csv')

}
slovar_layouts_level2 = {
    'границы': import_csv('data/level_graphics/lvl2_layouts/borders2.csv'),
    'монстры': import_csv('data/level_graphics/lvl2_layouts/monsters2.csv'),
}

player_animation = {
    'up': ['data/animations/main_charecter/up/up_1.png',
           'data/animations/main_charecter/up/up_2.png',
           'data/animations/main_charecter/up/up_3.png',
           'data/animations/main_charecter/up/up_4.png'
           ],
    'down': ['data/animations/main_charecter/down/down_1.png',
             'data/animations/main_charecter/down/down_2.png',
             'data/animations/main_charecter/down/down_3.png',
             'data/animations/main_charecter/down/down_4.png'
             ],

    'right': ['data/animations/main_charecter/right/right_1.png',
              'data/animations/main_charecter/right/right_2.png',
              'data/animations/main_charecter/right/right_3.png',
              'data/animations/main_charecter/right/right_4.png'
              ],

    'left': ['data/animations/main_charecter/left/left_1.png',
             'data/animations/main_charecter/left/left_2.png',
             'data/animations/main_charecter/left/left_3.png',
             'data/animations/main_charecter/left/left_4.png'
             ],
    'attack': {'up_attack': 'data/animations/main_charecter/attack/attack_up.png',
               'down_attack': 'data/animations/main_charecter/attack/attack_down.png',
               'left_attack': 'data/animations/main_charecter/attack/attack_left.png',
               'right_attack': 'data/animations/main_charecter/attack/attack_right.png',
               },

    'down_idle': 'data/animations/main_charecter/idle/main_idle.png',
    'up_idle': 'data/animations/main_charecter/idle/up_idle.png',
    'left_idle': 'data/animations/main_charecter/idle/left_idle.png',
    'right_idle': 'data/animations/main_charecter/idle/right_idle.png',
    'dead': 'data/animations/main_charecter/Dead.png'
}

weapons = {
    'lance': {'cooldown': 300,
              'damage': 25,
              'attack_cooldown': '',
              'image': ['data/weapons/lance_up.png',
                        'data/weapons/lance_down.png',
                        'data/weapons/lance_right.png',
                        'data/weapons/lance_left.png']
              }
}

monsters = {
    'bamboo': {'health': 100, 'damage': 15, 'type_attack': 'bamboo_attack', 'resistance': 2,
               'speed': 2, 'attack_radius': 50, 'notice_radius': 340, 'attack_cooldown': 800, 'exp': 10,
               'hit_sound': 'data/Sounds/Game/slash.wav',
               'idle': ['data/monsters/bamboo/idle_1.png',
                        'data/monsters/bamboo/idle_2.png',
                        'data/monsters/bamboo/idle_3.png',
                        'data/monsters/bamboo/idle_4.png',
                        ]
               },
    'slime': {'health': 125, 'damage': 25, 'type_attack': 'slash', 'resistance': 1,
              'speed': 3, 'attack_radius': 50, 'notice_radius': 360, 'attack_cooldown': 1200, 'exp': 20,
              'hit_sound': 'data/Sounds/Game/hit7.wav',
              'idle': ['data/monsters/slime/idle_1.png',
                       'data/monsters/slime/idle_2.png',
                       'data/monsters/slime/idle_3.png',
                       'data/monsters/slime/idle_4.png',
                       ],
              'dead': 'data/monsters/slime/dead.png'
              },
    'GiantSpirit': {'health': 300, 'damage': 35, 'type_attack': 'slash', 'resistance': 1,
                    'speed': 3, 'attack_radius': 120, 'notice_radius': 400, 'attack_cooldown': 1400, 'exp': 1000,
                    'hit_sound': 'data/Sounds/Game/hit7.wav',
                    'idle': ['data/monsters/GiantSpirit/idle_1.png',
                             'data/monsters/GiantSpirit/idle_2.png',
                             'data/monsters/GiantSpirit/idle_3.png',
                             'data/monsters/GiantSpirit/idle_4.png',
                             'data/monsters/GiantSpirit/idle_5.png'
                             ],
                    'hit': ['data/monsters/GiantSpirit/hit_1.png',
                            'data/monsters/GiantSpirit/hit_2.png',
                            'data/monsters/GiantSpirit/hit_3.png']
                    }
}

particles = {
    'leafs': [
        [
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00009.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00010.png'),
            pygame.image.load('data/Particles/leafs/leaf1/leaf1_00011.png'),
        ],
        [
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00002.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00009.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00010.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00011.png'),
            pygame.image.load('data/Particles/leafs/leaf2/leaf1_00012.png')
        ],

        [
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00002.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf3/leaf1_00009.png')
        ],

        [
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00002.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00009.png'),
            pygame.image.load('data/Particles/leafs/leaf4/leaf1_00010.png')

        ],

        [
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00002.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf5/leaf1_00009.png'),
        ],
        [
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00000.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00001.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00002.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00003.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00004.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00005.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00006.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00007.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00008.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00009.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00010.png'),
            pygame.image.load('data/Particles/leafs/leaf6/leaf1_00011.png'),
        ]
    ],
    'slash': [pygame.image.load('data/Particles/slash/0.png'),
              pygame.image.load('data/Particles/slash/1.png'),
              pygame.image.load('data/Particles/slash/2.png'),
              pygame.image.load('data/Particles/slash/3.png'),
              ],
    'bamboo_attack': [
        pygame.image.load('data/Particles/bamboo_attack/0.png'),
        pygame.image.load('data/Particles/bamboo_attack/1.png'),
        pygame.image.load('data/Particles/bamboo_attack/2.png'),
        pygame.image.load('data/Particles/bamboo_attack/3.png'),
        pygame.image.load('data/Particles/bamboo_attack/4.png'),
        pygame.image.load('data/Particles/bamboo_attack/5.png'),
        pygame.image.load('data/Particles/bamboo_attack/6.png'),

    ],
    'bamboo_death': [
        pygame.image.load('data/Particles/bamboo_death/0.png'),
        pygame.image.load('data/Particles/bamboo_death/1.png')
    ]
}

story_text = ['Это был обычный день в огромном мегаполисе.',
              'Я возвращался домой со своей собакой,',
              'как вдруг боковым зрением увидел',
              'летящую на огромной скорости в мою сторону',
              'машину!',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              'Похоже это конец...',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              'Однако очнувшись и кое как открыв глаза',
              'я увидел совершенно незнакомую местность',
              'Она не была похожа ни на что,',
              'что я раньше видел до этого',
              'Вокруг меня стояли люди ',
              'и что-то пытались мне сказать,',
              'но из-за звона в ушах, я их не слышал...']

dialog_icons = ['data/menu/player_photo.png', 'data/menu/master_photo.png']

start_dialog = [[dialog_icons[0], '(Что... что произошло!? Где я, и кто эти люди?)'],
                [dialog_icons[1], 'Приветстуем тебя воин.'],
                [dialog_icons[1], 'Мы являемся старейшинами этой деревни.'],
                [dialog_icons[1], 'Согласно нашим легендам ты - избранный герой'],
                [dialog_icons[1], 'который может победить злобного духа'],
                [dialog_icons[0], '(ГЕРОЙ!?) Как я могу быть героем?!...'],
                [dialog_icons[1], 'Ошибки быть не может'],
                [dialog_icons[1], 'Пожалуйста, исполни своё предназначение.'],
                [dialog_icons[0], '(Видимо, мне и впарвду надо будет его убить)'],
                [dialog_icons[0], 'Чтож, ладно...'],
                [dialog_icons[0], 'А где он находится?'],
                [dialog_icons[1], 'На северо-востоке от сюда, в заброшенной шахте.'],
                [dialog_icons[1], 'Но будь осторожен!'],
                [dialog_icons[1], 'Его преспешники скываются в лесах'],
                [dialog_icons[1], 'неподалёку от деревни.']]
end_text = ['Это конец.',
            'Теперь жителям деревни ничего не угрожает',
            'На их землях снова воцарил мир',
            '',
            '',
            '',
            'Итоговый результат:'
            ]

dead_text = ['Это конец.',
             'Вы не спавились с вашей великой миссией',
             'Теперь жители деревни обречены...',
             '',
             '',
             '',
             'Итоговый результат:',
             ]
