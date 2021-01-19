# Hibernate

A MCDR plugin which hibernates your server when no one's online, and resume it when someone login

## How to use

### As a player

1. Click the button *Refresh*
2. If you see the *favicon* is a bed, nevermind, connect to the server
3. Since the server is just starting, you may run into a connection error, but please be patient
4. Wait for a while, and click the button *Refresh* again
5. If the *favicon* has changed, or server status has changed to *Old Version!*,
   That means the server is ready! Connect again and enjoy your game!

## How it works

When there's no one online, Hibernate will do a count down.
If no one login during the count down, then Hibernate will shutdown the server.

When the server is down, Hibernate will act as a **FakeServer**, which keeps an
 eye on the MC port, for example, `25565`, and start the server when receiving
 a **login request**.

The **FakeServer** will also respond the player's **ping request**, and change
 the *MOTD*, the *favicon* as shown below.
> The **ping request** we meant here is the request sent by client when the 
> button *Refresh* is clicked.

## Features

- [x] Basic Features
- [x] Read Config
- [ ] In game setting
- [ ] Long connection
- [ ] Ping