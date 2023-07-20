import pygame
import random
import math

pygame.init()

class Draw:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    GRADIENT = [
        (12,4,4),
        (54,69,79),
        (26,26,33)
    ]

    FONT = pygame.font.SysFont('comicsans',30)
    LARGE_FONT = pygame.font.SysFont('comicsans',40)

    SIDE_PAD = 100
    TOP_PAD = 150
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Visualizor")
        self.set_lst(lst)

    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD)/(self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    
    return lst

def draw(draw_info,algo_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.BLACK)
    draw_info.window.blit(title,( draw_info.width/2 - title.get_width()/2,5))

    
    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting", 1, draw_info.BLACK)
    draw_info.window.blit(controls,( draw_info.width/2 - controls.get_width()/2,35))

    sorting = draw_info.FONT.render("Q - Quick Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting,( draw_info.width/2 - sorting.get_width()/2,65))
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {},clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD,draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)
    for i,val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENT[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color , (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

def pivot(draw_info, p, q):
    lst = draw_info.lst
    x = lst[p]
    i = p

    for j in range(p+1,q+1):
        if lst[j] <= x:
            i+=1
            (lst[i], lst[j]) = (lst[j], lst[i])
            draw_list(draw_info,{i: draw_info.GREEN,j: draw_info.RED},True)
            yield True
 
    (lst[p],lst[i]) = (lst[i],lst[p])
    draw_list(draw_info,{p: draw_info.GREEN,i: draw_info.RED},True)   
    yield True
    return i

def Quick_sort(draw_info, p, q):
    if p> q:
        yield True
        return
    
    
    mid = yield from pivot(draw_info,p,q)
    yield from Quick_sort(draw_info,p,mid-1)
    yield from Quick_sort(draw_info,mid+1,q)
    
def bubble_sort(draw_info):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            n1 = lst[j]
            n2 = lst[j+1]

            if n1>n2:
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j: draw_info.GREEN,j+1: draw_info.RED},True)
                yield True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n,min_val, max_val)
    draw_info = Draw(800,600, lst)
    sorting = False
    ascending = True
    descending = False

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else: 
            draw(draw_info,sorting_algo_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val, max_val)
                draw_info.set_lst(lst)
                sorting == False
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                if sorting_algo == Quick_sort:
                    sorting_algo_generator = sorting_algo(draw_info,0,len(draw_info.lst)-1)
                else: 
                    sorting_algo_generator = sorting_algo(draw_info)
            
            elif event.key == pygame.K_b and sorting == False:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
            
            elif event.key == pygame.K_q and sorting == False:
                sorting_algo = Quick_sort
                sorting_algo_name = "Quick Sort"
    
    pygame.quit()
    



if __name__ == "__main__":
    main()