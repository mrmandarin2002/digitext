package sample;

import sample.Interaction;

import java.io.IOException;
import java.net.SocketException;
import java.net.UnknownHostException;

class interaction_test {
    public static void main(String[] args) throws SocketException, UnknownHostException, IOException {
        Interaction client = new Interaction("127.0.0.1", 7356);
        System.out.println(client.valid_t("12345"));
        client.close();
    }
}