#include <winsock2.h>
#include <stdio.h>

int main()
{
  system("chcp 65001");
  SOCKET s;
  int port = 3124;

  /* Initailization */
  WSADATA wsa;
  WSAStartup(MAKEWORD(2,2), &wsa);

  struct sockaddr_in server;
  
  /* Create new socket */
  if((s = socket(PF_INET, SOCK_STREAM,0)) == INVALID_SOCKET)
    return WSAGetLastError();

  server.sin_family = AF_INET;
  server.sin_addr.s_addr = htonl(INADDR_ANY);
  server.sin_port = htons(port);

  /* Binding */
  if(bind(s, (struct sockaddr *)&server, sizeof(struct sockaddr)) == SOCKET_ERROR)
    return WSAGetLastError();

  /* Listening */
  listen(s, 10);

  SOCKET client;
  struct sockaddr_in client_addr;
  char *buffer;

  FILE *fp = fopen("0000201810", "r");
  fseek(fp, 0, SEEK_END);
  long fsize = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  buffer = (char *)malloc(fsize + 1);
  fread(buffer, fsize, 1, fp);
  fclose(fp);
  buffer[fsize] = 0;

  int c = sizeof(struct sockaddr_in);
  client = accept(s, (struct sockaddr *)&client_addr, &c);
  
  int send_amount = send(client, buffer, fsize,0);
  printf("sent : %d\n", send_amount);

  printf("%s\n",buffer);

  close(client);
  closesocket(s);
  WSACleanup();
  system("PAUSE");
}