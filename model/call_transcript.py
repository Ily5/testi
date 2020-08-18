class CallTranscript:
    bad_call = "але ну да что вы хотите да да да что вы хотите але не знаю у меня еще один есть " \
               "я звоню другим не знаю даже как вот ну с меня потом выдирать"

    neutral_call = "ало да давайте попробуем понятия не имею если честно давайте на пятёрке " \
                   "остановимся будет везде средний результат ставить а я говорю давайте пять поставим " \
                   "потому что я не вижу смысла повторять этот вопрос"

    good_call = "да здравствуйте мария ну давайте пару минут можно нет ну в настоящий момент десять " \
                "ну как бы больше никаких у меня трений не было все хорошо я что-то не" \
                " поняла просто мне все понравилось наоборот все хорошо "

    test_asr_1 = "ало да конечно я буквально вчера подключила его тариф этот я поменяла ммм понятно ээ давайте" \
                 "давайте я подумаю ещё "

    test_asr_2 = "але ой извините пока нет щас я на работе извините пожалуйста я просто никак сейчас угу так а" \
                 "а по цене это будет сколько коллер да он за этой стенкой будет в конце ряда они вот за этой " \
                 "стенкой в конце ряда слева будут там есть прям цвета разные "

    test_asr_3 = "алё ну да что вы хотите да да да что вы хотите а я им почти не пользуюсь не знаю у меня ещё один " \
                 "есть дак я звоню другим а что а что вы "

    test_asr_4 = "не знаю даже как уу а с меня потом выдирать ничего не будут ну давайте сохраняем если что " \
                 "отключиться же можно потом да алё отключиться то можно если что будет давайте давайте слышите" \
                 "нет алё "

    test_asr_5 = "ало хм смотря о чём ну да пока сижу на другой сим карте пока временно приостановила обслуживание " \
                 "ну это временно скоро будет это хорошо по истечении года нужно будет что отключать эту услугу "

    test_asr_6 = "да могу повторить ааа потом для отключения этой услуги ну всмысле через год она будет платная или " \
                 "она всё время будет платной вы говорите она действует один год правильно я поняла да давайте  " \
                 "спасибо досвидания "

    test_asr_7 = "ало ну не совсем а что "

    test_asr_8 = "не знаю да что да да да ну как бы вообще никуда не выезжаю редкий случай коронавирус да нет наверно " \
                 "не получится в ближайшее время угу "

    test_asr_9 = "ну не совсем конечно если недолго а что случилось не знаю даже может и получится пока не знаю"

    test_asr_10 = "алё угу ну если не долго алё ммм нет уже известно спасибо ну она в приложении была видна поэтому " \
                  "я видела мне она не нужнав данный момент мне хватает интернета который у меня есть что ещё  " \
                  "раз хорошо я я знаю об этом в приложениия я видела мне хватает того трафика который у меня есть "

    test_asr_11 = "ещё разочек да ой да я собственно говоря этот как сказать да я как то подключал себе такую штуку " \
                  "я не расходую так и так весь трафикв месяц нет смысла делать это "

    test_asr_12 = "алё нет угу да да да да до свидания"

    test_asr_13 = "алё добрый день я слушаю вас алё да слушаю спасибо да спасибо да спасибо вам большое"

    test_asr_14 = "да здравствуйте мария ну давайте пару минут можно нет ну в настоящий момент десять больше никаких " \
                  "у меня трений не было всё хорошо почему низкую то десять это что самая низкая что ли я что то не " \
                  "поняла мне всё понравилось наоборот всё хорошо проблем у меня нет никаких "

    test_asr_15 = "алё удобно один ну потому что тут это самое много чего у вас купил всё устроило мне " \
                  "не понравилась ситуация с чайником покупал у вас чайник вот и соответственно ээ это самое принёс " \
                  "его через шесть дней потому что как бы раньше не мог прийти я один раз его вскрипятил "

    test_asr_16 = "ну получается появилась эта самая ржавчина ну такие следы ржавчины как бы хотя как бы написано о " \
                  "том что чайник из нержавейки это самое мне отказались как бы при чём вот я пришёл как бы ну ведь " \
                  "не запрашивать возврат средств как бы именно осуществить замену товара на чайник со стеклянной " \
                  "колбой на что мне как бы был дан отказ "

    test_asr_17 = "алё здравствуйте давайте пять пять пять наверно по десятибальной ну дело в том что я делал у вас " \
                  "заказ три раза ну вот два раза его не привозили отменяли спасибо досвидания "

    test_asr_18 = "да алё угу ну такое четыре иногда тормозит оборудование ваше угу "

    test_asr_19 = "угу что вы хотели ало ну да у меня пока нет нет не будет пусть этот будет тариф это чё он " \
                  "бесплатный да будет ну потом не сейчас подождите я с работы пошла отдыхаю подумаю я ещё "

    test_asr_20 = "здрасте нет нет это не я это неверно нуу раз указано значит вы ошиблись а вам какая разница вы " \
                  "кто сначала представтесь вообще с чужого телефона звоните и мне не представляясь спрашиваете про " \
                  "каких то людей а я кто такой я я если вы не знаете кому вы звоните я должен вам объяснять не зная " \
                  "кто вы такой вообще "

    test_asr_21 = "какой корреспонденции ну всё я ему передам он придёт получит придёт получит заказное письмо а в " \
                  "чём дело то слушайте я не пойму какие данные я должен указать чьи то уточнять вы уточните сами чё " \
                  "проблема в чём вы заказное письмо заказали я должен уточнять чьи то данные у вас все данные есть " \
                  "на всё а мой телефон с какого хрена у него в контактах "

    test_asr_22 = "алё нет вы ошибаетесь не знаю девушка вы мне звонили нет вы мне на протяжении наверно полугода " \
                  "звонили я сказал что если ещё как бы будут меня тревожить что я в суд подам как бы вроде " \
                  "ос" \
                  "ановились я человека знать не знал но в итоге я с ним познакомился специально что бы его узнать "

    test_asr_23 = "алё м ну не очень а как что оплачивается не оплачивается тариф меняется что как оно вообще влияет " \
                  "да нет не надо мне как бы да нет вроде да нет нет пока не нужно  да не нужно не нет нет спасибо не" \
                  " нужно "

    test_asr_24 = "слушаю я слушаю вас нет  я же сказал нет нет нет я сказал нет нет нет нет ничего не добавляем нет " \
                  "нет "

    test_asr_25 = "ну удобно здравствуйте здравствуйте да у меня нету у меня нет интернета ой я не знаю я не знаю ещё " \ 
                  "у меня нет интернета я не пользуюсь интернетом "

    test_asr_26 = "да удобно здравствуйте очень давно понятненько услуга в месяц сколько оплачивается о не молодой " \
                  "человек меня это не устраивает меня мой тариф вполне устраивает вы меня слышите ало "

    test_asr_27 = "алё а по поводу чего да нет в принципе меня пока устраивает этот тариф который у меня есть мне " \
                  "хватает всего и минут и трафика смсками вообще не пользуюсь поэтому нет наверно ну пока пока я не " \
                  "буду ничего делать "

    test_asr_28 = "да удобно здравствуйте очень давно понятненько услуга в месяц сколько оплачивается о не молодой " \
                  "человек меня это не устраивает меня мой тариф вполне устраивает вы меня слышите ало "

    test_asr_29 = "алё а по поводу чего да нет в принципе меня пока устраивает этот тариф который у меня есть мне " \
                  "хватает всего и минут и трафика смсками вообще не пользуюсь поэтому нет наверно ну пока пока я не " \
                  "буду ничего делать "

    test_asr_30 = "ну я редко звоню просто я когда мне надо я звоню просто по работе я этой пользовался этой услугой " \
                  "но она мне что-то бонусы не возвращались мне на телефон на номер а деньги не будут за это " \
                  "сниматься ну давайте "

    test_asr_31 = "да здравствуйте ну да говорите всмысле давно не пользовался номером как это я им давно не " \
                  "пользовался дак они итак мне возвращаются ну она бесплатная или платная "

    test_asr_32 = "алё здравствуйте да удобно а в чём проблема как понять не пользовался я езжу не понял о чём речь " \
                  "что повторить хорошо хорошо"

    test_asr_33 = "ало да с каким именно у меня два у меня два на этом телефоне а ну не пользовалась ну просто у " \
                  "меня другой телефон я пока им не пользуюсь ну два номера два но с коронавирусом "

    test_asr_34 = "ало да всё что потребности нет я не хочу пользоваться пока а для чего ээ а какую сумму нужно " \
                  "потратить что бы был кеш бек там же определённую сумму нужно потратить или нет "

    test_asr_35 = "да ну вообще мы как бы пользуемся и вполне комфортно просто сейчас мы находимся в состоянии " \
                  "карантина ну как бы ну особенно звонков нет в основном пользуемся интернетом а так тарифный план " \
                  "полностью устраивает так нас полностью устраивает тараифный план мы бы не хотели его менять угу " \
                  "хорошо угу "

    test_asr_36 = "мм какую возможность ещё раз я не понял какую возможность что нужно для меня дак они итак мне " \
                  "возвращаются ммм ну она бесплатная или платная ну с меня будут списываться дополнительные деньги " \
                  "вы мне так скажите а "

    test_asr_37 = "мм какую возможность ещё раз я не понял какую возможность что нужно для меня дак они итак мне " \
                  "возвращаются ммм ну она бесплатная или платная ну с меня будут списываться дополнительные деньги " \
                  "вы мне так скажите а "

    test_asr_38 = "понятненько услуга в месяц сколько оплачивается о не молодой человек меня это не устраивает " \
                  "меня мой тариф вполне устраивает вы меня слышите ало ну я понимаю ну я плачу всего двести " \
                  "пятьдесят рублей в месяц у меня там сергей сергей послушайте пожалуйста я понимаю если было бы" \
                  " там до предела "

    test_asr_39 = "ну да у меня пока нет нет пусть этот будет тариф это чё он бесплатный да будет ну потом не сейчас " \
                  "подождите я с работы пришла отдыхаю подумаю я ещё ну кароче три тысячи будет ага и чего нада " \
                  "будет делать ага ага "

    test_asr_40 = "сергей сергей послушайте пожалуйста я понимаю если бы было бы до предела в пределах трёхсот " \
                  "рублей да я бы ещё бы с этим нет нет нет нет я не согласен потому что было бы в пределах трёхсот " \
                  "рублей я бы согласился а тут со скидкой двадцать процетов пятьсот рублей в месяц да не это не " \
                  "выгодно я плачу двести пятьдесят рублей меня всё устраивает "

    test_asr_41 = "а вы статистику смотрите потому что я платил одну сим карту а я пользуюсь двумя да я понимаю не " \
                  "всегда но в большинстве дак мне интернет всегда достаточно а пакеты мтс я не всегда ими пока " \
                  "скидка сколько будет оплата сколько вы сказали "

    test_asr_42 = "дак у меня тоже на тот тот же тариф тот тот же тариф у меня сейчас который имеется на данный " \
                  "момент безлимитный интернет и девятьсот минут да меня вполне устраивает я не готов сергей " \
                  "меня мой тариф вполне устраивает всего доброго досвидания вам "

    test_asr_43 = "дак у меня тоже на тот тот же тариф тот тот же тариф у меня сейчас который имеется на данный " \
                  "момент безлимитный интернет и девятьсот минут да меня вполне устраивает я не готов сергей " \
                  "меня мой тариф вполне устраивает всего доброго досвидания вам "

    test_asr_44 = "нет я на работе спасибо я доволен всем абсолютно всё время десять или пятьнадцать лет сколько " \
                  "двадцать лет я всё время с мегафоном желаю вам процветания всё да ну их на мегафон ну я не жалуюсь " \
                  "на них так то мтс хуже больше воруют деньги"

    test_asr_45 = "да могу повторить для потом для отключения этой услуги ну всмысле через год она будет платная или " \
                  "или она всё время будет бесплатная вы говорите она действует один год правильно я поняла да " \
                  "давайте спасибо досвидания  "

    test_asr_46 = "я не знаю я подумаю хорошо я попробую но я ещё подумаю ну да нет да нет да интернетом алё ой нет " \
                  "пока не нада нет я же не пользуюсь я же интернетом не пользуюсь нет я не буду нет пока я не хочу "


class Numbers:
    pass
