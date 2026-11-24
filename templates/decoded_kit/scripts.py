"""English scripts for the Decoded series. Each sentence is read in one TTS call (punctuation kept).
SENT: (chapter, sentence, [subtitle chunks]). HEADS: one headline per chapter: [(text, accent)]. LABEL: chapter word."""
EP = {}

EP[1] = dict(topic='FAKE PARCEL TEXT', music=1, SENT=[
 (0, "This text knows your name. Here's how.", ["This text knows your name.", "Here's how."]),
 (1, "Your name and number are already out there: hacked websites, online forms, resold lists.", ["Your name and number are already out there:", "hacked websites, online forms,", "resold lists."]),
 (2, "A bot sends the same message to thousands of people, with a link to a fake tracking page.", ["A bot sends the same message", "to thousands of people,", "with a link to a fake tracking page."]),
 (3, "You pay a small delivery fee… and you hand over your card.", ["You pay a small delivery fee…", "and you hand over your card."]),
 (4, "The rule: never pay through a link you got by text.", ["The rule:", "never pay through a link you got by text."]),
 (4, "Open the courier's app yourself.", ["Open the courier's app yourself."]),
 (4, "Share this with someone who's waiting for a parcel.", ["Share this with someone", "who's waiting for a parcel."]),
], HEADS=[[('This text knows', 0), ('your name.', 1)], [('Your data is', 0), ('already out there.', 1)],
          [('One message,', 0), ('thousands of phones.', 1)], [('A fake', 0), ('tracking page.', 1)], [('Never pay', 0), ('through a link.', 1)]])

EP[2] = dict(topic='FREE CAFÉ WI-FI', music=2, SENT=[
 (0, "This free Wi-Fi just slipped in between you and the internet.", ["This free Wi-Fi just slipped in", "between you and the internet."]),
 (1, "In a café, someone creates a network with the same name as the café's.", ["In a café, someone creates a network", "with the same name as the café's."]),
 (1, "Your phone connects to it on its own.", ["Your phone connects to it on its own."]),
 (2, "From now on, everything you send goes through their computer first.", ["From now on, everything you send", "goes through their computer first."]),
 (2, "It's called a man-in-the-middle attack.", ["It's called a man-in-the-middle attack."]),
 (3, "The padlock on websites protects a lot, but not everything.", ["The padlock on websites protects a lot,", "but not everything."]),
 (3, "The rule: use your phone's hotspot for anything sensitive, and forget networks you don't know.", ["The rule: use your phone's hotspot", "for anything sensitive,", "and forget networks you don't know."]),
], HEADS=[[('Free Wi-Fi,', 0), ('uninvited guest.', 1)], [('A second network,', 0), ('same name.', 1)],
          [('Everything goes', 0), ('through them.', 1)], [('Use your own', 0), ('connection.', 1)]])

EP[4] = dict(topic="THE BOSS'S VOICE", music=4, SENT=[
 (0, "Your director calls you for an urgent transfer. It isn't him.", ["Your director calls you", "for an urgent transfer.", "It isn't him."]),
 (1, "A few seconds of his voice are enough: a video, a voice note, an interview.", ["A few seconds of his voice are enough:", "a video, a voice note, an interview."]),
 (1, "An AI copies it.", ["An AI copies it."]),
 (2, "The call comes on a Friday evening. The tone is rushed, the amount is large, and he insists: \"it's confidential.\"", ["The call comes on a Friday evening.", "The tone is rushed, the amount is large,", "and he insists: \"it's confidential.\""]),
 (3, "The rule that protects you: no transfer without calling back on a known number, and a code word agreed between management and finance.", ["The rule that protects you:", "no transfer without calling back", "on a known number,", "and a code word agreed", "between management and finance."]),
 (3, "Send this to your accounting team.", ["Send this to your accounting team."]),
], HEADS=[[('It sounds like him.', 0), ("It isn't.", 1)], [('A few seconds', 0), ('are enough.', 1)],
          [('Urgent. Confidential.', 0), ('Friday evening.', 1)], [('Always', 0), ('call back.', 1)]])

EP[5] = dict(topic='DATA LEAK', music=5, SENT=[
 (0, "Your data leaked. Here's its journey to your phone.", ["Your data leaked.", "Here's its journey to your phone."]),
 (1, "In April 2025, the CNSS leak in Morocco was a reminder: a stolen database doesn't disappear.", ["In April 2025, the CNSS leak in Morocco", "was a reminder:", "a stolen database doesn't disappear."]),
 (2, "It's copied, sorted, and sold on.", ["It's copied, sorted, and sold on."]),
 (2, "Names, numbers, emails and employers get matched together.", ["Names, numbers, emails and employers", "get matched together."]),
 (3, "Then come targeted messages, mentioning your company or your bank.", ["Then come targeted messages,", "mentioning your company or your bank."]),
 (4, "Morocco's Law 09-08 requires companies to protect this data and declare it to the CNDP.", ["Morocco's Law 09-08 requires companies", "to protect this data", "and declare it to the CNDP."]),
 (4, "And you? Be wary of any message that knows a little too much.", ["And you?", "Be wary of any message", "that knows a little too much."]),
], HEADS=[[('Your data', 0), ('leaked.', 1)], [('A stolen database', 0), ("doesn't disappear.", 1)],
          [('Copied. Sorted.', 0), ('Matched.', 1)], [('A message that', 0), ('knows too much.', 1)], [('Law', 0), ('09-08.', 1)]])

EP[6] = dict(topic='THE META PIXEL', music=6, SENT=[
 (0, "You looked at a sofa. Instagram knows. How?", ["You looked at a sofa.", "Instagram knows. How?"]),
 (1, "The store's website contains a small invisible piece of code: the pixel.", ["The store's website contains", "a small invisible piece of code:", "the pixel."]),
 (2, "When you visit the page, it sends a signal to Meta: this person looked at this sofa.", ["When you visit the page,", "it sends a signal to Meta:", "this person looked at this sofa."]),
 (2, "Meta links that signal to your account.", ["Meta links that signal to your account."]),
 (3, "The store can then show you its ad, and show it to people like you.", ["The store can then show you its ad,", "and show it to people like you."]),
 (3, "Understanding ads also means using them better for your business.", ["Understanding ads also means", "using them better for your business."]),
], HEADS=[[('Instagram', 0), ('knows.', 1)], [('An invisible', 0), ('code.', 1)], [('The signal finds', 0), ('your account.', 1)], [('The ad', 0), ('finds you.', 1)]])

EP[7] = dict(topic='SIM SWAP', music=3, SENT=[
 (0, "Your account can be emptied without anyone touching your phone.", ["Your account can be emptied", "without anyone touching your phone."]),
 (1, "The fraudster gathers your information, poses as you with your mobile operator, and gets a new SIM card for your number.", ["The fraudster gathers your information,", "poses as you with your mobile operator,", "and gets a new SIM card for your number."]),
 (2, "Your phone loses signal. Theirs receives your texts, including your bank's codes.", ["Your phone loses signal.", "Theirs receives your texts,", "including your bank's codes."]),
 (3, "The rule: if your phone suddenly loses signal, call your operator right away.", ["The rule: if your phone", "suddenly loses signal,", "call your operator right away."]),
 (3, "And when you can, use an authenticator app instead of text codes.", ["And when you can,", "use an authenticator app", "instead of text codes."]),
], HEADS=[[('Emptied from', 0), ('a distance.', 1)], [('A new SIM,', 0), ('your number.', 1)], [('Your codes go', 0), ('elsewhere.', 1)], [('No signal?', 0), ('Call.', 1)]])

EP[8] = dict(topic='THE HTTPS PADLOCK', music=2, SENT=[
 (0, "The padlock doesn't mean the website is honest.", ["The padlock doesn't mean", "the website is honest."]),
 (1, "It means one thing: the connection between you and this site is encrypted. No one can read what you send along the way.", ["It means one thing:", "the connection between you and this site", "is encrypted.", "No one can read what you send", "along the way."]),
 (2, "But if the site is a fake, you send your data, encrypted, straight to the fraudster.", ["But if the site is a fake,", "you send your data, encrypted,", "straight to the fraudster."]),
 (3, "Getting a padlock is free and takes a few minutes.", ["Getting a padlock is free", "and takes a few minutes."]),
 (4, "The real habit: check the address, letter by letter.", ["The real habit:", "check the address, letter by letter."]),
], HEADS=[[('A padlock is not', 0), ('a guarantee.', 1)], [('A protected', 0), ('connection.', 1)], [('Protected…', 0), ('towards whom?', 1)],
          [('Anyone can', 0), ('get one.', 1)], [('Read the', 0), ('address.', 1)]])

EP[9] = dict(topic='PASSWORDS', music=5, SENT=[
 (0, "Your password is already on a list.", ["Your password is already on a list."]),
 (1, "Hackers don't guess letter by letter. They try lists of leaked passwords, then variations: a word, a year, an exclamation mark.", ["Hackers don't guess letter by letter.", "They try lists of leaked passwords,", "then variations:", "a word, a year, an exclamation mark."]),
 (2, "\"Morocco2026!\" follows every rule… and it's among the first guesses.", ["\"Morocco2026!\" follows every rule…", "and it's among the first guesses."]),
 (3, "What works: a long phrase, different for every site, kept in a password manager. And two-factor authentication everywhere.", ["What works: a long phrase,", "different for every site,", "kept in a password manager.", "And two-factor authentication everywhere."]),
 (3, "What does yours look like?", ["What does yours look like?"]),
], HEADS=[[('Already on', 0), ('a list.', 1)], [('Lists, not', 0), ('guesses.', 1)], [('Word + year +', 0), ('!', 1)], [('A long', 0), ('phrase.', 1)]])

EP[10] = dict(topic='QR CODE SCAM', music=1, SENT=[
 (0, "This QR code wasn't put there by the car park.", ["This QR code wasn't put there", "by the car park."]),
 (1, "A sticker is enough, placed over the real one.", ["A sticker is enough,", "placed over the real one."]),
 (2, "You scan to pay, the page looks like the official service, and you enter your card.", ["You scan to pay,", "the page looks like the official service,", "and you enter your card."]),
 (2, "A QR code hides the address: you can't read it before you scan.", ["A QR code hides the address:", "you can't read it before you scan."]),
 (3, "The habit: look at the address before opening it, be wary of stickers, and pay in the official app.", ["The habit: look at the address", "before opening it,", "be wary of stickers,", "and pay in the official app."]),
], HEADS=[[('Not the', 0), ('real code.', 1)], [('Stuck', 0), ('on top.', 1)], [('A fake', 0), ('payment page.', 1)], [('Read before', 0), ('you open.', 1)]])

EP[11] = dict(topic='RANSOMWARE', music=6, SENT=[
 (0, "Monday, 8 a.m. Every file in the company is encrypted.", ["Monday, 8 a.m.", "Every file in the company is encrypted."]),
 (1, "It often starts with an attachment, or a badly protected access.", ["It often starts with an attachment,", "or a badly protected access."]),
 (2, "The software spreads silently across the network, waits, then encrypts everything at once, connected backups included.", ["The software spreads silently", "across the network, waits,", "then encrypts everything at once,", "connected backups included."]),
 (2, "A ransom note appears.", ["A ransom note appears."]),
 (3, "The rule that saves you: three copies, on two different media, one of them offline. And test your restore regularly.", ["The rule that saves you: three copies,", "on two different media,", "one of them offline.", "And test your restore regularly."]),
 (3, "A backup you've never tested isn't a backup.", ["A backup you've never tested", "isn't a backup."]),
], HEADS=[[('Monday,', 0), ('8 a.m.', 1)], [('One', 0), ('attachment.', 1)], [('Everything,', 0), ('at once.', 1)], [('Three copies.', 0), ('One offline.', 1)]])

EP[12] = dict(topic='WHATSAPP ENCRYPTION', music=3, SENT=[
 (0, "Even WhatsApp can't read this message. Here's why.", ["Even WhatsApp can't read this message.", "Here's why."]),
 (1, "Your phone and your contact's phone each have their own keys.", ["Your phone and your contact's phone", "each have their own keys."]),
 (2, "The message is encrypted on your phone. It crosses the servers in an unreadable form.", ["The message is encrypted on your phone.", "It crosses the servers", "in an unreadable form."]),
 (3, "Only your contact's phone can decrypt it. That's end-to-end encryption.", ["Only your contact's phone can decrypt it.", "That's end-to-end encryption."]),
 (3, "What stays visible: who talks to whom, and when.", ["What stays visible:", "who talks to whom, and when."]),
], HEADS=[[('Even WhatsApp', 0), ("can't read it.", 1)], [('Each phone,', 0), ('its own keys.', 1)], [('It carries.', 0), ("It doesn't read.", 1)], [('Only the', 0), ('recipient.', 1)]])

EP[13] = dict(topic='HOW AI READS AN INVOICE', music=4, SENT=[
 (0, "A machine reads an invoice in a few seconds. Here's what it sees.", ["A machine reads an invoice in a few seconds.", "Here's what it sees."]),
 (1, "First, an image: pixels. It finds the areas of text and turns them into characters.", ["First, an image: pixels.", "It finds the areas of text", "and turns them into characters."]),
 (2, "Then it understands the structure: this is a supplier, this is a date, this is a total.", ["Then it understands the structure:", "this is a supplier, this is a date,", "this is a total."]),
 (3, "It checks: does the VAT match the total?", ["It checks:", "does the VAT match the total?"]),
 (4, "Then it files everything in your software, in the right place.", ["Then it files everything in your software,", "in the right place."]),
 (4, "That's exactly what Nodal does with your documents.", ["That's exactly what Nodal does", "with your documents."]),
], HEADS=[[('What a machine', 0), ('sees.', 1)], [('First,', 0), ('pixels.', 1)], [('Supplier. Date.', 0), ('Total.', 1)], [('Does the VAT', 0), ('match?', 1)], [('In the', 0), ('right place.', 1)]])

EP[14] = dict(topic='HOW AI WRITES', music=2, SENT=[
 (0, "An AI doesn't think like you. It guesses the next word.", ["An AI doesn't think like you.", "It guesses the next word."]),
 (1, "It has read an enormous amount of text.", ["It has read an enormous amount of text."]),
 (2, "For each word, it calculates which word is most likely to come next.", ["For each word, it calculates", "which word is most likely to come next."]),
 (3, "Then the next one. Then the next one. That's why it writes fast, and why it can be wrong with confidence.", ["Then the next one. Then the next one.", "That's why it writes fast,", "and why it can be wrong with confidence."]),
 (4, "The right way to use it: give it your company's context, and always check what matters.", ["The right way to use it:", "give it your company's context,", "and always check what matters."]),
], HEADS=[[('It guesses the', 0), ('next word.', 1)], [('Billions of', 0), ('sentences.', 1)], [('The most likely', 0), ('word.', 1)], [('Then the', 0), ('next one.', 1)], [('Context, then', 0), ('check.', 1)]])

EP[15] = dict(topic='THE API', music=1, SENT=[
 (0, "Your software doesn't talk to each other. It's missing a waiter.", ["Your software doesn't talk to each other.", "It's missing a waiter."]),
 (1, "At a restaurant, you don't talk to the cook.", ["At a restaurant, you don't talk to the cook."]),
 (2, "The waiter takes the order, brings it to the kitchen, and comes back with the dish.", ["The waiter takes the order,", "brings it to the kitchen,", "and comes back with the dish."]),
 (2, "An API is that waiter between two pieces of software: your till asks, your stock answers.", ["An API is that waiter", "between two pieces of software:", "your till asks, your stock answers."]),
 (3, "Without an API, you copy things by hand. With one, information flows on its own.", ["Without an API, you copy things by hand.", "With one, information flows on its own."]),
 (3, "Nodal is the waiter between your tools.", ["Nodal is the waiter between your tools."]),
], HEADS=[[("They don't", 0), ('talk.', 1)], [('You never talk', 0), ('to the cook.', 1)], [('Ask.', 0), ('Answer.', 1)], [('Information', 0), ('flows.', 1)]])

EP[16] = dict(topic='THE CLOUD', music=5, SENT=[
 (0, "Your files \"in the cloud\" are in a building. Which one?", ["Your files \"in the cloud\" are in a building.", "Which one?"]),
 (1, "The cloud is thousands of computers in data centres: in Europe, in the United States, or in Morocco.", ["The cloud is thousands of computers", "in data centres:", "in Europe, in the United States,", "or in Morocco."]),
 (2, "When you save a file, it travels to one of them, and it's copied several times.", ["When you save a file,", "it travels to one of them,", "and it's copied several times."]),
 (3, "For a Moroccan company, the question matters: where is your customers' data hosted?", ["For a Moroccan company, the question matters:", "where is your customers' data hosted?"]),
 (3, "Law 09-08 regulates its transfer abroad. Ask your providers.", ["Law 09-08 regulates its transfer abroad.", "Ask your providers."]),
], HEADS=[[('A very physical', 0), ('cloud.', 1)], [('Thousands of', 0), ('computers.', 1)], [('Copied', 0), ('several times.', 1)], [('Where is', 0), ('your data?', 1)]])

EP[17] = dict(topic='THE INSTAGRAM FEED', music=6, SENT=[
 (0, "This post didn't end up here by chance.", ["This post didn't end up here by chance."]),
 (1, "Every time you open Instagram, thousands of posts are candidates.", ["Every time you open Instagram,", "thousands of posts are candidates."]),
 (2, "For each one, the app estimates how likely you are to watch it, like it, share it or save it.", ["For each one, the app estimates", "how likely you are to watch it,", "like it, share it or save it."]),
 (3, "It relies on what you did before: accounts you follow, time spent, messages. Then it ranks.", ["It relies on what you did before:", "accounts you follow, time spent, messages.", "Then it ranks."]),
 (4, "For a business, the lesson is simple: shares and saves weigh a lot. Save this post, and see.", ["For a business, the lesson is simple:", "shares and saves weigh a lot.", "Save this post, and see."]),
], HEADS=[[('Not by', 0), ('chance.', 1)], [('Thousands of', 0), ('candidates.', 1)], [('Watch. Like.', 0), ('Share. Save.', 1)], [('What you', 0), ('did before.', 1)], [('Then it', 0), ('ranks.', 1)]])

EP[18] = dict(topic='DARIJA AND AI', music=4, SENT=[
 (0, "\"Bghit nbdl lmaw3id.\" How does a machine understand that?", ["\"Bghit nbdl lmaw3id.\"", "How does a machine understand that?"]),
 (1, "Darija is written in Latin letters, in Arabic, and with numbers: 3 for the ayn, 9 for the qaf.", ["Darija is written in Latin letters,", "in Arabic, and with numbers:", "3 for the ayn, 9 for the qaf."]),
 (2, "An AI doesn't look for exact words. It learned meaning from examples: nbdl, change, move, all end up in the same place.", ["An AI doesn't look for exact words.", "It learned meaning from examples:", "nbdl, change, move,", "all end up in the same place."]),
 (3, "It understands the intent, changing an appointment, then it offers time slots.", ["It understands the intent,", "changing an appointment,", "then it offers time slots."]),
 (3, "Connection number one is coming soon.", ["Connection number one is coming soon."]),
], HEADS=[[('Bghit nbdl', 0), ('lmaw3id.', 1)], [('3 = ayn.', 0), ('9 = qaf.', 1)], [('Meaning,', 0), ('not words.', 1)], [('Time slots,', 0), ('right away.', 1)]])

EP[19] = dict(topic='THE UPDATE', music=3, SENT=[
 (0, "\"Later\" is a hacker's favourite button.", ["\"Later\" is a hacker's favourite button."]),
 (1, "An update often fixes a security flaw.", ["An update often fixes a security flaw."]),
 (2, "As soon as it's released, the flaw becomes known, and hackers know exactly what to attack in devices that weren't updated.", ["As soon as it's released,", "the flaw becomes known,", "and hackers know exactly what to attack", "in devices that weren't updated."]),
 (3, "A zero-day is worse: a flaw no one knows about yet, except the attacker.", ["A zero-day is worse:", "a flaw no one knows about yet,", "except the attacker."]),
 (4, "The best defence stays the same: update fast, everywhere, phones included. Turn on automatic updates tonight.", ["The best defence stays the same:", "update fast, everywhere, phones included.", "Turn on automatic updates tonight."]),
], HEADS=[[('The tempting', 0), ('button.', 1)], [('An update', 0), ('fixes a flaw.', 1)], [('The flaw becomes', 0), ('known.', 1)], [('Known to', 0), ('one person.', 1)], [('Update.', 0), ('Everywhere.', 1)]])

EP[20] = dict(topic='E-INVOICING', music=6, SENT=[
 (0, "Soon, the tax authority will see your invoice before your customer does.", ["Soon, the tax authority will see", "your invoice before your customer does."]),
 (1, "With e-invoicing, an invoice no longer goes out as a PDF by email.", ["With e-invoicing, an invoice", "no longer goes out as a PDF by email."]),
 (2, "It's sent in a structured format to a platform, checked, then passed on to your customer.", ["It's sent in a structured format", "to a platform, checked,", "then passed on to your customer."]),
 (3, "The exact timeline depends on the implementing texts. What won't change: you need clean data in your software.", ["The exact timeline depends", "on the implementing texts.", "What won't change:", "you need clean data in your software."]),
 (3, "IDs, VAT, invoice numbers. Get ready now, not the day before.", ["IDs, VAT, invoice numbers.", "Get ready now, not the day before."]),
], HEADS=[[('Before your', 0), ('customer.', 1)], [('No more', 0), ('PDF by email.', 1)], [('Through the', 0), ('platform.', 1)], [('Clean', 0), ('data.', 1)]])
