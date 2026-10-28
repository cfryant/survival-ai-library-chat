SURVIVAL KIT - START HERE
=========================
Everything in this folder runs from this USB drive. No internet, no installing.
It works on any Windows 10/11 PC: plug in the drive and use the files below.

1) THE GUIDES (always works, even without the AI)
   Open:  Survival Library\INDEX.html
   Your official PDF guides (e.g. CDC, FEMA, Red Cross, WHO, US Army, IFRC, ...)
   sorted into topic folders such as first aid, water, food, power outages,
   carbon monoxide and fire, winter storms, floods, wilderness survival,
   sanitation, family plans, communications.

2) THE OFFLINE AI ASSISTANT
   Open the "AI" folder and double-click:
     Start Survival AI (battery).bat      <- use this one normally (small 4B model)
     Start Survival AI (plugged in).bat   <- bigger 9B model, better answers, more power
     Start Survival AI (lowest power, built-in GPU).bat  <- 4B on the built-in (integrated) GPU
                                             so a discrete GPU can sleep (slower)
     Stop Survival AI.bat                 <- ALWAYS run this when you are done

   After 10-60 seconds your browser opens the LIBRARY CHAT
   (http://127.0.0.1:8081). It searches the guides for every question, answers
   from them, lists the sources, and lets you click a source to open that PDF
   at the right page. The file path is shown too, so you can also open it from
   the Survival Library folder by hand.
   The plain AI chat (no library search) is at http://127.0.0.1:8080. There you
   can attach a guide PDF with the + button so the AI reads it.
   Both run only on this computer (127.0.0.1); nothing is sent anywhere.
   If the AI will not start, the guides in step 1 still work.

3) SAVING BATTERY
   - Turn on Windows Battery Saver (Settings > System > Power & battery).
   - Close other apps (browsers tabs, games, Discord, Steam, etc.).
   - Use the battery launcher, or the "lowest power, built-in GPU" launcher.
   - Run "Stop Survival AI.bat" when you are not asking questions.
     (The AI also unloads itself after 5 idle minutes, but stopping is better.)
   - Dim the screen. Keep questions short.
   - Read the PDFs directly when you can - that uses the least power.
   - If you have a phone or power bank, the PDFs can be copied to it too.

4) IMPORTANT
   The AI can be wrong. Its answers are NOT medical certainty.
   The official guides win - always check the guide it cites.
   In a real emergency call 911 (or your local emergency number) if you can.

Rebuild the AI's library search after adding guides:
   AI\library-search\Rebuild library index.bat
