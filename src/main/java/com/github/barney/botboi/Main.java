package com.github.barney.botboi;

import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;

public class Main
{

	public static void main(String[] args)
	{
		String token = "NDE2NDA2NDg3MDI0NDAyNDMy.DuQ1zw.LCfFiK4uneZ6z9Odb3jL4ddGNTw";

        DiscordApi api = new DiscordApiBuilder().setToken(token).login().join();
        System.out.println("\nLogged in as " + api.getClientId());
	}
	


}
