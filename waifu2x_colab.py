import os
import subprocess
from datetime import datetime
from google.colab import files
from google.colab import drive
!git clone https://github.com/tsurumeso/waifu2x-chainer


horario1 = str(datetime.now()).split()[1].split(".")[0]
try:
  drive.mount('/content/drive/')
except:
  exit()


def video_upload():
    global numero
    print()
    numero = int(input('[1] Localfile \n[2] Google Drive \n \nSelecione um número: '))
    if numero == 1:
      try:
        try:
          files.upload()

        except:
          files.upload()
      except:
        print("Erro ao inciar serviço de upload!\n")
        print("Reinicie...")
        quit()
    else:
      pass


def print_dir():
    global diretorio, novoindice, scale, caminho

    indice = 1
    if numero == 1:
      caminho = "/content/"
    else:
      caminho = "/content/drive/My Drive/"
    diretorio = os.listdir(caminho)

    for item in diretorio:
      print([indice], item)
      indice += 1
    
    print()
    novoindice = int(input("\nSelecione o seu arquivo: ")) - 1
    scale = int(input("\nNúmero de vezes que deseja ampliar: "))
    print()
    

def get_fps():
    global fps

    fps = str(os.popen(f'ffmpeg -i "{caminho}{diretorio[novoindice]}" 2> fps.txt ; egrep -i "fps" fps.txt').read())
    fps = fps.split(",")[4].split()[0]
    !rm "fps.txt"


def get_frames():
    try:
      os.system(f"mkdir frames")
    except:
      pass

    print("Extraindo frames e audio do seu vídeo...")
    os.system(f'cd frames && ffmpeg -i "{caminho}{diretorio[novoindice]}" %d.png')
    os.system(f'cd frames && ffmpeg -i "{caminho}{diretorio[novoindice]}" -vn -acodec copy /content/audio.aac')


def upscale_frames():
    print()
    print("Realizando upscale de cada imagem...")
    %cd /content/waifu2x-chainer
    !python waifu2x.py -m noise_scale -n 2 -s {scale} -i /content/frames -a 0 -g 0  > /dev/null 2>&1


def move_upscale_frames():
    %cd /content
    path = "/content/waifu2x-chainer"
    file_list = os.listdir(path)
    file_list.sort()

    for numero in range(0, len(file_list)):
        file_list[numero] = f"{path}/{file_list[numero]}"

    try:
        os.system("mkdir upframes")
    except:
        pass

    cont = 0
    for item in file_list:
        if item != f"{path}/appendix" and item != f"{path}/images" and item != f"{path}/LICENSE" and item != f"{path}/README.md" and item != f"{path}/waifu2x.py" and item != f"{path}/lib" and item != f"{path}/models" and item != f"{path}/train.py" and item != f"{path}/.flake8" and item != f"{path}/.git" and item != f"{path}/.gitignore" and item != f"{path}/read2x.py" and item != f"{path}/upframes":
            subprocess.Popen(["mv", item, "upframes"])
            cont += 1

    print()
    print(cont, "itens movidos para /content/upframes")


def generating_video2x():
    global obra

    %cd /content/upframes
    print()
    print("Gerando novo arquivo de vídeo...")
    obra = f"{diretorio[novoindice][0:-4]}_upscale.mkv"
    os.system(f"""ffmpeg -f image2 -r {fps} -i %d.png -i /content/audio.aac '/content/drive/My Drive/{diretorio[novoindice][0:-4]}_upscale.mkv' """)
    print('\n==================== FIIIIIIIIIMMMMMMMMMMMM ====================')
    print()


horario2 = str(datetime.now()).split()[1].split(".")[0]


if __name__ == "__main__":
    video_upload()
    print_dir()
    get_fps()
    get_frames()
    upscale_frames()
    move_upscale_frames()
    generating_video2x()
    print(horario1)
    print(horario2)
    !rm -r frames upframes 

    #send_for_drive()
   
