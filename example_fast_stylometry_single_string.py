'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/fast-stylometry-python-library/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from faststylometry import Corpus

from faststylometry import download_examples
from faststylometry import load_corpus_from_folder
from faststylometry import tokenise_remove_pronouns_en
from faststylometry import calculate_burrows_delta
from faststylometry import predict_proba, calibrate, get_calibration_curve

download_examples()

train_corpus = load_corpus_from_folder("data/train")

train_corpus.tokenise(tokenise_remove_pronouns_en)


test_corpus = Corpus()

test_corpus.add_book("currerbell", "villette", """My godmother lived in a handsome house in the clean and ancient town of Bretton. Her husband’s family had been residents there for generations, and bore, indeed, the name of their birthplace—Bretton of Bretton: whether by coincidence, or because some remote ancestor had been a personage of sufficient importance to leave his name to his neighbourhood, I know not.

When I was a girl I went to Bretton about twice a year, and well I liked the visit. The house and its inmates specially suited me. The large peaceful rooms, the well-arranged furniture, the clear wide windows, the balcony outside, looking down on a fine antique street, where Sundays and holidays seemed always to abide—so quiet was its atmosphere, so clean its pavement—these things pleased me well.

One child in a household of grown people is usually made very much of, and in a quiet way I was a good deal taken notice of by Mrs. Bretton, who had been left a widow, with one son, before I knew her; her husband, a physician, having died while she was yet a young and handsome woman.

She was not young, as I remember her, but she was still handsome, tall, well-made, and though dark for an Englishwoman, yet wearing always the clearness of health in her brunette cheek, and its vivacity in a pair of fine, cheerful black eyes. People esteemed it a grievous pity that she had not conferred her complexion on her son, whose eyes were blue—though, even in boyhood, very piercing—and the colour of his long hair such as friends did not venture to specify, except as the sun shone on it, when they called it golden. He inherited the lines of his mother’s features, however; also her good teeth, her stature (or the promise of her stature, for he was not yet full-grown), and, what was better, her health without flaw, and her spirits of that tone and equality which are better than a fortune to the possessor.

In the autumn of the year —— I was staying at Bretton; my godmother having come in person to claim me of the kinsfolk with whom was at that time fixed my permanent residence. I believe she then plainly saw events coming, whose very shadow I scarce guessed; yet of which the faint suspicion sufficed to impart unsettled sadness, and made me glad to change scene and society.

Time always flowed smoothly for me at my godmother’s side; not with tumultuous swiftness, but blandly, like the gliding of a full river through a plain. My visits to her resembled the sojourn of Christian and Hopeful beside a certain pleasant stream, with “green trees on each bank, and meadows beautified with lilies all the year round.” The charm of variety there was not, nor the excitement of incident; but I liked peace so well, and sought stimulus so little, that when the latter came I almost felt it a disturbance, and wished rather it had still held aloof.

One day a letter was received of which the contents evidently caused Mrs. Bretton surprise and some concern. I thought at first it was from home, and trembled, expecting I know not what disastrous communication: to me, however, no reference was made, and the cloud seemed to pass.

The next day, on my return from a long walk, I found, as I entered my bedroom, an unexpected change. In, addition to my own French bed in its shady recess, appeared in a corner a small crib, draped with white; and in addition to my mahogany chest of drawers, I saw a tiny rosewood chest. I stood still, gazed, and considered.

“Of what are these things the signs and tokens?” I asked. The answer was obvious. “A second guest is coming: Mrs. Bretton expects other visitors.”

On descending to dinner, explanations ensued. A little girl, I was told, would shortly be my companion: the daughter of a friend and distant relation of the late Dr. Bretton’s. This little girl, it was added, had recently lost her mother; though, indeed, Mrs. Bretton ere long subjoined, the loss was not so great as might at first appear. Mrs. Home (Home it seems was the name) had been a very pretty, but a giddy, careless woman, who had neglected her child, and disappointed and disheartened her husband. So far from congenial had the union proved, that separation at last ensued—separation by mutual consent, not after any legal process. Soon after this event, the lady having over-exerted herself at a ball, caught cold, took a fever, and died after a very brief illness. Her husband, naturally a man of very sensitive feelings, and shocked inexpressibly by too sudden communication of the news, could hardly, it seems, now be persuaded but that some over-severity on his part—some deficiency in patience and indulgence—had contributed to hasten her end. He had brooded over this idea till his spirits were seriously affected; the medical men insisted on travelling being tried as a remedy, and meanwhile Mrs. Bretton had offered to take charge of his little girl. “And I hope,” added my godmother in conclusion, “the child will not be like her mamma; as silly and frivolous a little flirt as ever sensible man was weak enough to marry. For,” said she, “Mr. Home is a sensible man in his way, though not very practical: he is fond of science, and lives half his life in a laboratory trying experiments—a thing his butterfly wife could neither comprehend nor endure; and indeed” confessed my godmother, “I should not have liked it myself.”

In answer to a question of mine, she further informed me that her late husband used to say, Mr. Home had derived this scientific turn from a maternal uncle, a French savant; for he came, it seems; of mixed French and Scottish origin, and had connections now living in France, of whom more than one wrote de before his name, and called himself noble.

That same evening at nine o’clock, a servant was despatched to meet the coach by which our little visitor was expected. Mrs. Bretton and I sat alone in the drawing-room waiting her coming; John Graham Bretton being absent on a visit to one of his schoolfellows who lived in the country. My godmother read the evening paper while she waited; I sewed. It was a wet night; the rain lashed the panes, and the wind sounded angry and restless.

“Poor child!” said Mrs. Bretton from time to time. “What weather for her journey! I wish she were safe here.”

A little before ten the door-bell announced Warren’s return. No sooner was the door opened than I ran down into the hall; there lay a trunk and some band-boxes, beside them stood a person like a nurse-girl, and at the foot of the staircase was Warren with a shawled bundle in his arms.

“Is that the child?” I asked.

“Yes, miss.”

I would have opened the shawl, and tried to get a peep at the face, but it was hastily turned from me to Warren’s shoulder.

“Put me down, please,” said a small voice when Warren opened the drawing-room door, “and take off this shawl,” continued the speaker, extracting with its minute hand the pin, and with a sort of fastidious haste doffing the clumsy wrapping. The creature which now appeared made a deft attempt to fold the shawl; but the drapery was much too heavy and large to be sustained or wielded by those hands and arms. “Give it to Harriet, please,” was then the direction, “and she can put it away.” This said, it turned and fixed its eyes on Mrs. Bretton.

“Come here, little dear,” said that lady. “Come and let me see if you are cold and damp: come and let me warm you at the fire.”

The child advanced promptly. Relieved of her wrapping, she appeared exceedingly tiny; but was a neat, completely-fashioned little figure, light, slight, and straight. Seated on my godmother’s ample lap, she looked a mere doll; her neck, delicate as wax, her head of silky curls, increased, I thought, the resemblance.

Mrs. Bretton talked in little fond phrases as she chafed the child’s hands, arms, and feet; first she was considered with a wistful gaze, but soon a smile answered her. Mrs. Bretton was not generally a caressing woman: even with her deeply-cherished son, her manner was rarely sentimental, often the reverse; but when the small stranger smiled at her, she kissed it, asking, “What is my little one’s name?”

“Missy.”

“But besides Missy?”

“Polly, papa calls her.”

“Will Polly be content to live with me?”

“Not always; but till papa comes home. Papa is gone away.” She shook her head expressively.

“He will return to Polly, or send for her.”

“Will he, ma’am? Do you know he will?”

“I think so.”

“But Harriet thinks not: at least not for a long while. He is ill.”

Her eyes filled. She drew her hand from Mrs. Bretton’s and made a movement to leave her lap; it was at first resisted, but she said—“Please, I wish to go: I can sit on a stool.”

She was allowed to slip down from the knee, and taking a footstool, she carried it to a corner where the shade was deep, and there seated herself. Mrs. Bretton, though a commanding, and in grave matters even a peremptory woman, was often passive in trifles: she allowed the child her way. She said to me, “Take no notice at present.” But I did take notice: I watched Polly rest her small elbow on her small knee, her head on her hand; I observed her draw a square inch or two of pocket-handkerchief from the doll-pocket of her doll-skirt, and then I heard her weep. Other children in grief or pain cry aloud, without shame or restraint; but this being wept: the tiniest occasional sniff testified to her emotion. Mrs. Bretton did not hear it: which was quite as well. Ere long, a voice, issuing from the corner, demanded—“May the bell be rung for Harriet!”

I rang; the nurse was summoned and came.

“Harriet, I must be put to bed,” said her little mistress. “You must ask where my bed is.”

Harriet signified that she had already made that inquiry.

“Ask if you sleep with me, Harriet.”

“No, Missy,” said the nurse: “you are to share this young lady’s room,” designating me.

Missy did not leave her seat, but I saw her eyes seek me. After some minutes’ silent scrutiny, she emerged from her corner.

“I wish you, ma’am, good night,” said she to Mrs. Bretton; but she passed me mute.

“Good-night, Polly,” I said.

“No need to say good-night, since we sleep in the same chamber,” was the reply, with which she vanished from the drawing-room. We heard Harriet propose to carry her up-stairs. “No need,” was again her answer—“no need, no need:” and her small step toiled wearily up the staircase.

On going to bed an hour afterwards, I found her still wide awake. She had arranged her pillows so as to support her little person in a sitting posture: her hands, placed one within the other, rested quietly on the sheet, with an old-fashioned calm most unchildlike. I abstained from speaking to her for some time, but just before extinguishing the light, I recommended her to lie down.

“By and by,” was the answer.

“But you will take cold, Missy.”

She took some tiny article of raiment from the chair at her crib side, and with it covered her shoulders. I suffered her to do as she pleased. Listening awhile in the darkness, I was aware that she still wept,—wept under restraint, quietly and cautiously.

On awaking with daylight, a trickling of water caught my ear. Behold! there she was risen and mounted on a stool near the washstand, with pains and difficulty inclining the ewer (which she could not lift) so as to pour its contents into the basin. It was curious to watch her as she washed and dressed, so small, busy, and noiseless. Evidently she was little accustomed to perform her own toilet; and the buttons, strings, hooks and eyes, offered difficulties which she encountered with a perseverance good to witness. She folded her night-dress, she smoothed the drapery of her couch quite neatly; withdrawing into a corner, where the sweep of the white curtain concealed her, she became still. I half rose, and advanced my head to see how she was occupied. On her knees, with her forehead bent on her hands, I perceived that she was praying.

Her nurse tapped at the door. She started up.

“I am dressed, Harriet,” said she; “I have dressed myself, but I do not feel neat. Make me neat!”

“Why did you dress yourself, Missy?”

“Hush! speak low, Harriet, for fear of waking the girl” (meaning me, who now lay with my eyes shut). “I dressed myself to learn, against the time you leave me.”

“Do you want me to go?”

“When you are cross, I have many a time wanted you to go, but not now. Tie my sash straight; make my hair smooth, please.”

“Your sash is straight enough. What a particular little body you are!”

“It must be tied again. Please to tie it.”

“There, then. When I am gone you must get that young lady to dress you.”

“On no account.”

“Why? She is a very nice young lady. I hope you mean to behave prettily to her, Missy, and not show your airs.”

“She shall dress me on no account.”

“Comical little thing!”

“You are not passing the comb straight through my hair, Harriet; the line will be crooked.”

“Ay, you are ill to please. Does that suit?”

“Pretty well. Where should I go now that I am dressed?”

“I will take you into the breakfast-room.”

“Come, then.”

They proceeded to the door. She stopped.

“Oh! Harriet, I wish this was papa’s house! I don’t know these people.”

“Be a good child, Missy.”

“I am good, but I ache here;” putting her hand to her heart, and moaning while she reiterated, “Papa! papa!”

I roused myself and started up, to check this scene while it was yet within bounds.

“Say good-morning to the young lady,” dictated Harriet. She said, “Good-morning,” and then followed her nurse from the room. Harriet temporarily left that same day, to go to her own friends, who lived in the neighbourhood.

On descending, I found Paulina (the child called herself Polly, but her full name was Paulina Mary) seated at the breakfast-table, by Mrs. Bretton’s side; a mug of milk stood before her, a morsel of bread filled her hand, which lay passive on the table-cloth: she was not eating.

“How we shall conciliate this little creature,” said Mrs. Bretton to me, “I don’t know: she tastes nothing, and by her looks, she has not slept.”

I expressed my confidence in the effects of time and kindness.

“If she were to take a fancy to anybody in the house, she would soon settle; but not till then,” replied Mrs. Bretton.

CHAPTER II.
PAULINA.
Some days elapsed, and it appeared she was not likely to take much of a fancy to anybody in the house. She was not exactly naughty or wilful: she was far from disobedient; but an object less conducive to comfort—to tranquillity even—than she presented, it was scarcely possible to have before one’s eyes. She moped: no grown person could have performed that uncheering business better; no furrowed face of adult exile, longing for Europe at Europe’s antipodes, ever bore more legibly the signs of home sickness than did her infant visage. She seemed growing old and unearthly. I, Lucy Snowe, plead guiltless of that curse, an overheated and discursive imagination; but whenever, opening a room-door, I found her seated in a corner alone, her head in her pigmy hand, that room seemed to me not inhabited, but haunted.

And again, when of moonlight nights, on waking, I beheld her figure, white and conspicuous in its night-dress, kneeling upright in bed, and praying like some Catholic or Methodist enthusiast—some precocious fanatic or untimely saint—I scarcely know what thoughts I had; but they ran risk of being hardly more rational and healthy than that child’s mind must have been.

I seldom caught a word of her prayers, for they were whispered low: sometimes, indeed, they were not whispered at all, but put up unuttered; such rare sentences as reached my ear still bore the burden, “Papa; my dear papa!” This, I perceived, was a one-idea’d nature; betraying that monomaniac tendency I have ever thought the most unfortunate with which man or woman can be cursed.

What might have been the end of this fretting, had it continued unchecked, can only be conjectured: it received, however, a sudden turn.

One afternoon, Mrs. Bretton, coaxing her from her usual station in a corner, had lifted her into the window-seat, and, by way of occupying her attention, told her to watch the passengers and count how many ladies should go down the street in a given time. She had sat listlessly, hardly looking, and not counting, when—my eye being fixed on hers—I witnessed in its iris and pupil a startling transfiguration. These sudden, dangerous natures—sensitive as they are called—offer many a curious spectacle to those whom a cooler temperament has secured from participation in their angular vagaries. The fixed and heavy gaze swum, trembled, then glittered in fire; the small, overcast brow cleared; the trivial and dejected features lit up; the sad countenance vanished, and in its place appeared a sudden eagerness, an intense expectancy. “It is!” were her words.

Like a bird or a shaft, or any other swift thing, she was gone from the room. How she got the house-door open I cannot tell; probably it might be ajar; perhaps Warren was in the way and obeyed her behest, which would be impetuous enough. I—watching calmly from the window—saw her, in her black frock and tiny braided apron (to pinafores she had an antipathy), dart half the length of the street; and, as I was on the point of turning, and quietly announcing to Mrs. Bretton that the child was run out mad, and ought instantly to be pursued, I saw her caught up, and rapt at once from my cool observation, and from the wondering stare of the passengers. A gentleman had done this good turn, and now, covering her with his cloak, advanced to restore her to the house whence he had seen her issue.

I concluded he would leave her in a servant’s charge and withdraw; but he entered: having tarried a little while below, he came up-stairs.

His reception immediately explained that he was known to Mrs. Bretton. She recognised him; she greeted him, and yet she was fluttered, surprised, taken unawares. Her look and manner were even expostulatory; and in reply to these, rather than her words, he said,—“I could not help it, madam: I found it impossible to leave the country without seeing with my own eyes how she settled.”

“But you will unsettle her.”

“I hope not. And how is papa’s little Polly?”

This question he addressed to Paulina, as he sat down and placed her gently on the ground before him.

“How is Polly’s papa?” was the reply, as she leaned on his knee, and gazed up into his face.

It was not a noisy, not a wordy scene: for that I was thankful; but it was a scene of feeling too brimful, and which, because the cup did not foam up high or furiously overflow, only oppressed one the more. On all occasions of vehement, unrestrained expansion, a sense of disdain or ridicule comes to the weary spectator’s relief; whereas I have ever felt most burdensome that sort of sensibility which bends of its own will, a giant slave under the sway of good sense.

Mr. Home was a stern-featured—perhaps I should rather say, a hard-featured man: his forehead was knotty, and his cheekbones were marked and prominent. The character of his face was quite Scotch; but there was feeling in his eye, and emotion in his now agitated countenance. His northern accent in speaking harmonised with his physiognomy. He was at once proud-looking and homely-looking. He laid his hand on the child’s uplifted head. She said—“Kiss Polly.”

He kissed her. I wished she would utter some hysterical cry, so that I might get relief and be at ease. She made wonderfully little noise: she seemed to have got what she wanted—all she wanted, and to be in a trance of content. Neither in mien nor in features was this creature like her sire, and yet she was of his strain: her mind had been filled from his, as the cup from the flagon.

Indisputably, Mr. Home owned manly self-control, however he might secretly feel on some matters. “Polly,” he said, looking down on his little girl, “go into the hall; you will see papa’s great-coat lying on a chair; put your hand into the pockets, you will find a pocket-handkerchief there; bring it to me.”

She obeyed; went and returned deftly and nimbly. He was talking to Mrs. Bretton when she came back, and she waited with the handkerchief in her hand. It was a picture, in its way, to see her, with her tiny stature, and trim, neat shape, standing at his knee. Seeing that he continued to talk, apparently unconscious of her return, she took his hand, opened the unresisting fingers, insinuated into them the handkerchief, and closed them upon it one by one. He still seemed not to see or to feel her; but by-and-by, he lifted her to his knee; she nestled against him, and though neither looked at nor spoke to the other for an hour following, I suppose both were satisfied.

During tea, the minute thing’s movements and behaviour gave, as usual, full occupation to the eye. First she directed Warren, as he placed the chairs.

“Put papa’s chair here, and mine near it, between papa and Mrs. Bretton: I must hand his tea.”

She took her own seat, and beckoned with her hand to her father.

“Be near me, as if we were at home, papa.”

And again, as she intercepted his cup in passing, and would stir the sugar, and put in the cream herself, “I always did it for you at home; papa: nobody could do it as well, not even your own self.”

Throughout the meal she continued her attentions: rather absurd they were. The sugar-tongs were too wide for one of her hands, and she had to use both in wielding them; the weight of the silver cream-ewer, the bread-and-butter plates, the very cup and saucer, tasked her insufficient strength and dexterity; but she would lift this, hand that, and luckily contrived through it all to break nothing. Candidly speaking, I thought her a little busy-body; but her father, blind like other parents, seemed perfectly content to let her wait on him, and even wonderfully soothed by her offices.

“She is my comfort!” he could not help saying to Mrs. Bretton. That lady had her own “comfort” and nonpareil on a much larger scale, and, for the moment, absent; so she sympathised with his foible.

This second “comfort” came on the stage in the course of the evening. I knew this day had been fixed for his return, and was aware that Mrs. Bretton had been expecting him through all its hours. We were seated round the fire, after tea, when Graham joined our circle: I should rather say, broke it up—for, of course, his arrival made a bustle; and then, as Mr. Graham was fasting, there was refreshment to be provided. He and Mr. Home met as old acquaintance; of the little girl he took no notice for a time.

His meal over, and numerous questions from his mother answered, he turned from the table to the hearth. Opposite where he had placed himself was seated Mr. Home, and at his elbow, the child. When I say child I use an inappropriate and undescriptive term—a term suggesting any picture rather than that of the demure little person in a mourning frock and white chemisette, that might just have fitted a good-sized doll—perched now on a high chair beside a stand, whereon was her toy work-box of white varnished wood, and holding in her hands a shred of a handkerchief, which she was professing to hem, and at which she bored perseveringly with a needle, that in her fingers seemed almost a skewer, pricking herself ever and anon, marking the cambric with a track of minute red dots; occasionally starting when the perverse weapon—swerving from her control—inflicted a deeper stab than usual; but still silent, diligent, absorbed, womanly.

Graham was at that time a handsome, faithless-looking youth of sixteen. I say faithless-looking, not because he was really of a very perfidious disposition, but because the epithet strikes me as proper to describe the fair, Celtic (not Saxon) character of his good looks; his waved light auburn hair, his supple symmetry, his smile frequent, and destitute neither of fascination nor of subtlety (in no bad sense). A spoiled, whimsical boy he was in those days.

“Mother,” he said, after eyeing the little figure before him in silence for some time, and when the temporary absence of Mr. Home from the room relieved him from the half-laughing bashfulness, which was all he knew of timidity—-“Mother, I see a young lady in the present society to whom I have not been introduced.”

“Mr. Home’s little girl, I suppose you mean,” said his mother.

“Indeed, ma’am,” replied her son, “I consider your expression of the least ceremonious: Miss Home I should certainly have said, in venturing to speak of the gentlewoman to whom I allude.”

“Now, Graham, I will not have that child teased. Don’t flatter yourself that I shall suffer you to make her your butt.”

“Miss Home,” pursued Graham, undeterred by his mother’s remonstrance, “might I have the honour to introduce myself, since no one else seems willing to render you and me that service? Your slave, John Graham Bretton.”

She looked at him; he rose and bowed quite gravely. She deliberately put down thimble, scissors, work; descended with precaution from her perch, and curtsying with unspeakable seriousness, said, “How do you do?”

“I have the honour to be in fair health, only in some measure fatigued with a hurried journey. I hope, ma’am, I see you well?”

“Tor-rer-ably well,” was the ambitious reply of the little woman and she now essayed to regain her former elevation, but finding this could not be done without some climbing and straining—a sacrifice of decorum not to be thought of—and being utterly disdainful of aid in the presence of a strange young gentleman, she relinquished the high chair for a low stool: towards that low stool Graham drew in his chair.

“I hope, ma’am, the present residence, my mother’s house, appears to you a convenient place of abode?”

“Not par-tic-er-er-ly; I want to go home.”

“A natural and laudable desire, ma’am; but one which, notwithstanding, I shall do my best to oppose. I reckon on being able to get out of you a little of that precious commodity called amusement, which mamma and Mistress Snowe there fail to yield me.”

“I shall have to go with papa soon: I shall not stay long at your mother’s.”

“Yes, yes; you will stay with me, I am sure. I have a pony on which you shall ride, and no end of books with pictures to show you.”

“Are you going to live here now?”

“I am. Does that please you? Do you like me?”

“No.”

“Why?”

“I think you queer.”

“My face, ma’am?”

“Your face and all about you: You have long red hair.”

“Auburn hair, if you please: mamma, calls it auburn, or golden, and so do all her friends. But even with my ‘long red hair’” (and he waved his mane with a sort of triumph—tawny he himself well knew that it was, and he was proud of the leonine hue), “I cannot possibly be queerer than is your ladyship.”

“You call me queer?”

“Certainly.”

(After a pause), “I think I shall go to bed.”

“A little thing like you ought to have been in bed many hours since; but you probably sat up in the expectation of seeing me?”

“No, indeed.”

“You certainly wished to enjoy the pleasure of my society. You knew I was coming home, and would wait to have a look at me.”

“I sat up for papa, and not for you.”

“Very good, Miss Home. I am going to be a favourite: preferred before papa soon, I daresay.”

She wished Mrs. Bretton and myself good-night; she seemed hesitating whether Graham’s deserts entitled him to the same attention, when he caught her up with one hand, and with that one hand held her poised aloft above his head. She saw herself thus lifted up on high, in the glass over the fireplace. The suddenness, the freedom, the disrespect of the action were too much.

“For shame, Mr. Graham!” was her indignant cry, “put me down!”—and when again on her feet, “I wonder what you would think of me if I were to treat you in that way, lifting you with my hand“ (raising that mighty member) “as Warren lifts the little cat.”

So saying, she departed.
""")

test_corpus.tokenise(tokenise_remove_pronouns_en)

bd = calculate_burrows_delta(train_corpus, test_corpus, vocab_size = 50)

print ("*** BURROWS DELTA VALUES ***")
print (bd)

calibrate(train_corpus)

probas = predict_proba(train_corpus, test_corpus)
print ("*** PROBABILITIES ***")
print (probas)
