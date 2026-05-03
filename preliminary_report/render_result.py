import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import sys

# Script pour générer l'image du puzzle 3DSRP
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

color1 = '#3a6ea5' # Bleu profond
color2 = '#548c5a' # Vert profond

# Z=0
grid_z0 = [[color2, color2],
           [color2, color1]]
text_z0 = [['', ''],
           ['1', '2']]

# Z=1
grid_z1 = [[color2, color1],
           [color1, color1]]
text_z1 = [['2', '1'],
           ['', '']]

def draw_grid(ax, grid, text, title):
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    
    for x in range(2):
        for y in range(2):
            color = grid[1-y][x]
            t = text[1-y][x]
            rect = patches.Rectangle((x, y), 1, 1, linewidth=3, edgecolor='#222222', facecolor=color, alpha=0.85)
            ax.add_patch(rect)
            
            # Subtle inner border for 3D/tile effect
            inner_rect = patches.Rectangle((x+0.05, y+0.05), 0.9, 0.9, linewidth=1, edgecolor='white', facecolor='none', alpha=0.3)
            ax.add_patch(inner_rect)
            
            if t:
                # Placer un cercle jaune pour le symbole (rappelant l'image de l'utilisateur)
                circle = patches.Circle((x+0.5, y+0.5), 0.25, facecolor='#f1c40f', edgecolor='#d4ac0d', linewidth=2)
                ax.add_patch(circle)
                ax.text(x+0.5, y+0.48, t, ha='center', va='center', fontsize=22, fontweight='bold', color='#333333')

draw_grid(axes[0], grid_z0, text_z0, "Layer Z=0 (Bottom)")
draw_grid(axes[1], grid_z1, text_z1, "Layer Z=1 (Top)")

# Indiquer les murs bloquants (Walls)
axes[0].text(0.5, 0.15, '⛔ Wall to Z=1', ha='center', va='center', fontsize=12, color='white', fontweight='bold', bbox=dict(facecolor='red', alpha=0.8, edgecolor='none', pad=2, boxstyle='round,pad=0.2'))
axes[0].text(1.5, 1.85, '⛔ Wall to Z=1', ha='center', va='center', fontsize=12, color='white', fontweight='bold', bbox=dict(facecolor='red', alpha=0.8, edgecolor='none', pad=2, boxstyle='round,pad=0.2'))

plt.tight_layout()
plt.savefig('result.png', dpi=300, facecolor='#ffffff')
print("Image result.png has been generated successfully.")
