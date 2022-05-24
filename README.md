# VKR
•	Telegram_Bot – модуль, который отвечает за получение сообщений и отправку сообщений клиенту через социальную сеть “telegram.” 
•	Main – модуль, выполняющий роль главного сервера и отвечающий за вызов модулей в правильном порядке. 
•	NLP – модуль, предназначенный для обработки текстового запроса пользователя. В этом модуле будет обрабатываться запрос пользователя по технологии NLP.
•	Products_handler – Модуль, отвечающий за обработку данных по товарам организации. Он приводит данные к удобному виду для построения графовой БД – определяет, какие параметры будут в начале и в конце графа, а также разбивает числовые параметры на группы для сокращения количества узлов в графе и, следовательно, для ускорения обработки запроса пользователя. 
•	Net_Generator – Модуль, предназначенный для формирования графовой базы данных В этом модуле программа будет строить графовую базу данных по обработанному CSV-файлу продукта для дальнейшего поиска максимально похожего под запрос пользователя товара.
•	Net_walking – Модуль поиска нужного товара в графовой БД. Он будет выполнять функцию поиска продукта по запросу клиента в уже построенной базе данных, путешествовать по графу, опираясь на ключевые слова из запроса клиента.
•	Extra_question - Модуль для генерации дополнительных вопросов при невозможности нахождения пути в графовой БД. 
Таким образом получается 7 модулей. Для того, чтобы в последствии не запутаться в их связи друг с другом, необходимо построить UML-диаграмму модулей и их связей. 
Unified Modeling Language (UML) – единый стандарт для построения модели любою системы. Их можно использовать для отображения связей баз данных, модулей проектов, связей экранов приложений и т. д. При наличии такой диаграммы программистам будет легче писать код, ведь связи между модулями осуществляется именно во время написания кода. Построенная UML-диаграмма показана на рисунке 2.4. При этом связь между модулями соответствует паттерну проектирования BFF и все модули, кроме Product_handler и Net_Generator связаны через REST API. 
 
Рис. 2.4. UML-диаграмма модулей и связей между ними
![image](https://user-images.githubusercontent.com/55450516/170057502-b999a3ef-4e6c-4a99-908c-42216ea07ec3.png)


