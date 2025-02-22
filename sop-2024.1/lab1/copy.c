#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#define SIZE 128

int myopen (const char *filename, int flags, int mode);
ssize_t myread(int fd, char *buf);
ssize_t mywrite(int fd, const char *buf);
int myclose(int fd);

int myopen (const char *filename, int flags, int mode) {
  // return open(filename, flags);
  // int fd = 0;
  ssize_t response;

  //r: 64 bits
  //e: 32 bits

  __asm__ ("mov %0, %%rdi" : : "r"(filename));
  __asm__ ("mov %0, %%esi" : : "d"(flags));
  __asm__ ("mov %0, %%edx" : : "d"(mode));
  __asm__ ("mov $2, %rax");
  __asm__ ("syscall");
  __asm__ ("mov %%rax, %0": "=r"(response) : );


  return response;
}

ssize_t myread(int fd, char *buf) {
  //return read(fd, buf, SIZE);

  ssize_t response;

  __asm__ ("mov %0, %%rdi" : : "r"(fd));
  __asm__ ("mov %0, %%esi" : : "d"(buf));
  __asm__ ("mov $0, %rax");
  __asm__ ("syscall");
  __asm__ ("mov %%rax, %0": "=r"(response) : );


  return response;

}
ssize_t mywrite(int fd, const char *buf) {
  // return write(fd, buf, count);

  ssize_t response;

  __asm__ ("mov %0, %%rdi" : : "r"(fd));
  __asm__ ("mov %0, %%esi" : : "d"(buf));
  __asm__ ("mov $1, %rax");
  __asm__ ("syscall");
  __asm__ ("mov %%rax, %0": "=r"(response) : );


  return response;
}

int myclose(int fd) {
  // return close(fd);

  ssize_t response;

  __asm__ ("mov %0, %%rdi" : : "r"(fd));
  __asm__ ("mov $3, %rax");
  __asm__ ("syscall");
  __asm__ ("mov %%rax, %0": "=r"(response) : );


  return response;

}

int main (int argc, char** argv) {

  int file;
  char buf[SIZE];
  ssize_t readCount;

  if (argc != 2) {
    fprintf(stderr,"correct usage: %s <filename>\n", argv[0]);
    return 1;
  }

  file = myopen (argv[1], O_RDONLY, SIZE);
  if (file<0) { perror("file open"); return 1;}

  while ((readCount = myread (file, buf)) > 0)
    if ((mywrite (STDOUT_FILENO, buf) != readCount))
      { perror("write"); return 1;}

  myclose (file);
  return 0;

}

