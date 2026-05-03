import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_3d_render():
    fig = plt.figure(figsize=(10, 8))
    # We use a highly controlled axis for the 3D projection
    ax = fig.add_subplot(111, projection='3d')
    
    # Force orthographic projection to exactly mimic the 2.5D CAD style of the friend's report
    ax.set_proj_type('ortho') 

    N = 3
    x, y, z = np.indices((N, N, N))

    # Dense, beautiful shape matching the style
    # R1: Vivid Orange (Left/Bottom)
    R1 = (
        ((x==0) & (y==0) & (z==0)) |
        ((x==1) & (y==0) & (z==0)) |
        ((x==0) & (y==1) & (z==0)) |
        ((x==0) & (y==0) & (z==1)) |
        ((x==1) & (y==0) & (z==1))
    )

    # R2: Deep Sky Blue (Top/Right)
    R2 = (
        ((x==1) & (y==1) & (z==1)) |
        ((x==2) & (y==1) & (z==1)) |
        ((x==1) & (y==2) & (z==1)) |
        ((x==1) & (y==1) & (z==2)) |
        ((x==2) & (y==1) & (z==2))
    )

    voxels = R1 | R2

    # Matplotlib Voxel rendering
    fc = np.empty(voxels.shape, dtype=object)
    fc[R1] = '#F05A28' # Professional Orange
    fc[R2] = '#1877F2' # Professional Blue

    ax.voxels(voxels, facecolors=fc, edgecolor='black', linewidth=1.5)

    # Draw the Background Grid (Wireframe) matching the friend's style!
    # By default in azim=-45, elev=25:
    # Viewer is at small x, small y. Front corner is (0,0,0).
    # The "back" planes are x=N, y=N, and the floor is z=0.
    grid_color = '#cbd5e1'
    grid_lw = 0.8
    
    # 1. Floor Grid (z=0)
    for i in range(N+1):
        ax.plot([i, i], [0, N], [0, 0], color=grid_color, lw=grid_lw, zorder=-1)
        ax.plot([0, N], [i, i], [0, 0], color=grid_color, lw=grid_lw, zorder=-1)
        
    # 2. Back-Left Wall (y=N)
    for i in range(N+1):
        ax.plot([i, i], [N, N], [0, N], color=grid_color, lw=grid_lw, zorder=-1)
        ax.plot([0, N], [N, N], [i, i], color=grid_color, lw=grid_lw, zorder=-1)
        
    # 3. Back-Right Wall (x=N)
    for i in range(N+1):
        ax.plot([N, N], [i, i], [0, N], color=grid_color, lw=grid_lw, zorder=-1)
        ax.plot([N, N], [0, N], [i, i], color=grid_color, lw=grid_lw, zorder=-1)

    # Add the puzzle symbols directly onto the exposed faces for 3DSRP
    # R1 Front symbols
    ax.text(1.5, -0.1, 0.5, r'$\bigstar$', size=30, color='black', ha='center', va='center')
    ax.text(0.5, 0.5, 1.5, r'$\bullet$', size=40, color='black', ha='center', va='center')

    # R2 Top/Side symbols
    ax.text(2.5, 1.5, 2.1, r'$\bigstar$', size=30, color='black', ha='center', va='center')
    ax.text(1.5, 0.9, 2.5, r'$\bullet$', size=40, color='black', ha='center', va='center')

    # Add red wall separating adjacent faces to satisfy the W constraint visually
    # Between R1 (1,0,1) and R2 (1,1,1) -> plane y=1 at x \in [1,2], z \in [1,2]
    ax.plot([1, 2], [1, 1], [1, 1], color='#DC2626', linewidth=5)
    ax.plot([1, 1], [1, 1], [1, 2], color='#DC2626', linewidth=5)

    # Strictly set bounds to prevent strange scaling
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_zlim(0, N)

    # Perfect isometric angle
    ax.view_init(elev=25, azim=-45)
    ax.set_axis_off()

    plt.tight_layout()
    output_path = '/Users/abdelouahad/Downloads/Project_KRR_ALLA-Odan-main/final_report/result_pro.png'
    plt.savefig(output_path, dpi=400, bbox_inches='tight', transparent=True)
    print(f"CAD-Style 3D render generated at: {output_path}")

if __name__ == '__main__':
    generate_3d_render()
