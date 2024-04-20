# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:48:36 2024

@author: clara
"""

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()
ecrits = rng.normal(14.3, 1.8, size=8000)
ecos = rng.normal(13.2, 2.4, size=8000) 
note_totale = 0.7*ecrits + 0.3*ecos


plt.figure()
plt.hist(ecrits, bins=np.arange(0,20,0.5),alpha=0.8, label = 'Notes écrits')
plt.hist(ecos,  bins=np.arange(0,20,0.5), alpha=0.8,label = 'Notes ECOS')
plt.hist(note_totale,  bins=np.arange(0,20,0.5), alpha=0.5, label = 'Notes totale')
plt.legend()
plt.title('Distribution des notes, pas de correlation')


# Pas de correlation

ecrits_ranking = scipy.stats.rankdata(-ecrits)
ecos_ranking = scipy.stats.rankdata(-ecos)
note_totale_ranking = scipy.stats.rankdata(-note_totale)

rank_diff = note_totale_ranking-ecrits_ranking

plt.figure()
plt.hist(rank_diff,  100)
plt.title('Distribution des variations de classement, sans corrélation')
plt.xlabel('Nombre de places perdues/gagnées')

print(np.percentile(rank_diff, 25))
print(np.percentile(rank_diff, 50))
print(np.percentile(rank_diff, 75) )
print(np.percentile(rank_diff, 90) )

plt.figure()
plt.scatter(ecrits_ranking, ecos_ranking, alpha=0.5)
coef_corr_rnd = np.corrcoef(ecrits_ranking, ecos_ranking)[0][1]
plt.title('Correlation ecrits-ECOS : r= %s' % np.round(coef_corr_rnd,3))
plt.xlabel('classement écrits')
plt.ylabel('classement ECOS')



# Avec correlation

ecos_ranked = np.sort(ecos)[::-1]
notes_ecos_matched_list = []
for a,x in enumerate(ecrits_ranking):
    # print('--------------------------------------')
    # print('note ecrit : ', ecrits[a])
    # print('rang ecrit : ', x)

    proba = rng.normal(x, 4000, size=20000)
    ''' Pour modififier la corrélation écrit-ecos, modifier le 2e argument. Plus bas= plus corrélé'''
    
    density = np.histogram(proba, bins=np.arange(0,8001), density=True)
    note_ecos_matched = np.random.choice(ecos_ranked, p = density[0])
    
    # print('note ecos matched : ', note_ecos_matched)
    
    notes_ecos_matched_list.append(note_ecos_matched)
notes_ecos_matched = np.array(notes_ecos_matched_list)
note_totale = 0.7*ecrits + 0.3*notes_ecos_matched


plt.figure()
plt.hist(ecrits, bins=np.arange(0,20,0.5), alpha=0.8, label = 'Notes écrits')
plt.hist(notes_ecos_matched_list,  bins=np.arange(0,20,0.5), alpha=0.8,  label = 'Notes ECOS')
plt.hist(note_totale,  bins=np.arange(0,20,0.5), alpha=0.5,  label = 'Notes totale')
plt.legend()
plt.title('Distribution des notes, correlation partielle')

note_totale_ranking = scipy.stats.rankdata(-note_totale)
ecos_matched_ranking = scipy.stats.rankdata(-notes_ecos_matched)

rank_diff = note_totale_ranking-ecrits_ranking
plt.figure()
plt.hist(rank_diff,  100)
plt.title('Distribution des variations de classement, correlation partielle')
plt.xlabel('Nombre de places perdues/gagnées')

print(np.percentile(rank_diff, 25) )
print(np.percentile(rank_diff, 50) )
print(np.percentile(rank_diff, 75) )
print(np.percentile(rank_diff, 90) )

plt.figure()
plt.scatter(ecrits_ranking, ecos_matched_ranking, alpha=0.3)
coef_corr = np.corrcoef(ecrits_ranking, ecos_matched_ranking)[0][1]
plt.title('Correlation ecrits-ECOS : r= %s' % np.round(coef_corr,3))
plt.xlabel('classement écrits')
plt.ylabel('classement ECOS')

plt.figure()
# plt.scatter(note_totale_ranking,rank_diff, alpha=0.5)
plt.scatter(ecrits_ranking,rank_diff, alpha=0.2)
plt.xlabel('Classement écrits')
plt.ylabel('Variation du classement')
plt.title ('Variation de classement selon le classement aux écrits')
