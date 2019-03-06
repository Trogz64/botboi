package com.github.barney.botboi;

import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;

public class Main
{

	public static void main(String[] args)
	{
		String token = "your token";

        DiscordApi api = new DiscordApiBuilder().setToken(token).login().join();
	}

}
