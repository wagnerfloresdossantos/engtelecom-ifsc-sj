package org.example;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.net.Socket;


public record Cliente(Socket conexao, BufferedReader entrada, DataOutputStream saida ) {}
