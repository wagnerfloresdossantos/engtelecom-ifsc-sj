#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <dirent.h>

/*
MYSHELL WAGNER
*/


int mycwd() {
  // char *getcwd(char buf[.size], size_t size);

  size_t size = PATH_MAX;
  char buf[size];

  if (getcwd(buf,sizeof(buf)) != NULL) {
    printf("%s\n", buf);
  } else {
    perror("getcwd() error\n");
    return 1;
  }
  return 0;
}

int mymkdir() {
  // int mkdir(const char *pathname, mode_t mode);

  char  pathname[PATH_MAX];
  printf("Novo diretório: ");
  scanf("%s", pathname);

  int retorno = mkdir(pathname, 0700);
  if(retorno != 0){
    perror("mkdir() error\n");
    return 1;
  }
  return 0;
}

int myrmdir() {
  // int rmdir(const char *pathname);
  
  char pathname[PATH_MAX];
  printf("Nome do diretório a ser deletado: ");
  scanf("%s", pathname);

  int retorno = rmdir(pathname);
  if(retorno != 0){
    perror("rmdir() error\n");
    return 1;
  }
  return 0;
}

int mycd() {
  // int chdir(const char *path);

  char pathname[PATH_MAX];
  scanf("%s", pathname);
  int retorno = chdir(pathname);
  if(retorno != 0){
    perror("chdir() error\n");
  } else {
    printf("Diretório alterado para: %s\n", pathname);
  }
  return 0;  
}

int mystat() {
  // int stat(const char *restrict pathname, struct stat *restrict statbuf);
 
  char pathname[PATH_MAX];
  struct stat arquivo;
  int size = arquivo.st_size;
  
  scanf("%s", pathname);
  int retorno = stat(pathname, &arquivo);
  if(retorno != 0){
    perror("stat() error\n");
  } else {
    printf("Tamanho do arquivo %s: %d bytes\n", pathname, size);
  }
  return 0; 
}

int myls() {
  // DIR *opendir(const char *name);

  struct dirent *dir; 
  DIR *d;
  
  char name[256];
  printf("Diretório a listar: ");
  scanf("%s", &name);

  d = opendir(name);
  if(d != NULL){
      while ((dir = readdir(d)) != NULL) {
        printf("%s/n", dir->d_name);
      }
      closedir(d);
    } else {
      printf("Diretório %s não encontrado", name);
      return 1;
    }
  
  return 0;
}

int main(int argc, char** argv) {
  int test = 0;
  while(test == 0) {
    char in[60];
    printf("myshell> ");
    scanf("%s", in);
  
    if(strcmp(in, "exit") == 0) {
      test = 1;
    } else if(strcmp(in, "cwd") == 0) {
      mycwd();
    } else if(strcmp(in, "mkdir") == 0) {
      mymkdir();
    } else if(strcmp(in, "rmdir") == 0) {
      myrmdir();
    } else if(strcmp(in, "cd") == 0) {
      mycd();
    } else if(strcmp(in, "stat") == 0) {
      mystat();
    } else if(strcmp(in, "ls") == 0) {
      myls();
    } else {
      printf("Comando não encontrado\n");
    }
  }
}
