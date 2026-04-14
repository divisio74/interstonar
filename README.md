utilisa tion de la focntion np.array de la lib numpy pour avoir des vecteur en trois dimensions

le resulttat de la formule de calcul est en Newton

structure du global :

boucle for 1000

 chaque item charger -> calcul les forces qui s'exercent sur chacun deux a frame t = 1
  
  appliquer les forces sur chaque object 

  if (objects a la meme position que le rock  )
    fin du programme = colision
  if (2 obejcts non rock a la meme psotion )
    fusion  -> quel trajectoire garder ?
    print rock->position



CalculForAll calcule juste la force totale, mais ne bouge rien.

COURS: 

Rappel de physique
Newton + Euler, c'est 3 étapes :

1. Force → Accélération
Seconde loi de Newton :


F = m × a    →    a = F / m
L'accélération d'un corps est la force qu'il subit divisée par sa masse.

Unités : F en N (= kg·m/s²), m en kg → a en m/s².

2. Accélération → Vitesse (Euler)
L'accélération, c'est "combien la vitesse change par seconde". Donc sur un petit intervalle dt :


new_vel = old_vel + a × dt
3. Vitesse → Position (Euler)
Pareil : la vitesse, c'est "combien la position change par seconde" :


new_pos = old_pos + new_vel × dt
