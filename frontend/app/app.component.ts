import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
  <nav>
    <a href="#"><img src="img/consolidated.png" alt="consolidated return">Сводный отчет</a>
    <a href="#"><img src="img/kpi.png" alt="operators KPI analysis">Оценка операторов<img src="img/nav-open.png" alt="close submeny" /></a>
    <a href="#" class="nav-active">Мастер отчетов</a>
    <a href="#">Настройки</a>
    <a href="#"><img src="img/loyalty.png" alt="clients loyalty">Лояльность клиентов<img src="img/nav-close.png" alt="open submeny" /></a>
    <a href="#"><img src="img/audiometry.png" alt="speech audiometry">Речевая аналитика</a>
    <a href="#"><img src="img/reference.png" alt="reference">Реферальная программа</a>
    <a href="#"><img src="img/support.png" alt="support">Поддержка</a>
    <a href="#"><img src="img/billings.png" alt="billings">Биллинг</a>
    <a href="#"><img src="img/settings.png" alt="settings">Настройки</a>
    <a href="#"><img src="img/exit.png" alt="exit">Выход</a>
  </nav>

  <main>
    <div class="navbar dialogue-nav">
      <ul class="navbar-nav">
        <li>Мастер отчетов</li>
        <li>Настройки</li>
      </ul>
      <div>
        <span class="date-range">11 ноя 2018 длинное тире 11 янв 2017</span>
        <ul>
          <li>Сегодня</li><li>Вчера</li><li>Неделя</li><li>Месяц</li><li>Квартал</li><li>Год</li>
        </ul>
      </div>
    </div>
    <div class="dialogue-face-list">
      <img src="img/settings_white.png" alt="settings">
      <h2>Сохраненные отчеты</h2>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span class="dialogue-face-list-active">Сейчас открыт</span>
      <span>Ещё срез</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
      <span>По статусам</span>
      <span>По тегам</span>
      <span>Отчеты по дням недели</span>
      <span>Звонки по часам</span>
    </div>
    <div>
      <img src="img/speech_chart_demos_temp_solution.png" alt="speech chart demos" style="width:100%" />
    </div>

    <div style="padding: 0px; background-color: white; overflow: visible;">
    	<dialogue-view></dialogue-view>
    </div>
  </main>



<script type="text/javascript">
        var progressScale = d3.scale.linear().range(["#63be7b", "#ffd963","#fc5456"]).domain([10,6,1]);
        d3.selectAll(".progress-bar").style("background-color", function() { return progressScale(this.style.width.slice(0,-2)); });
        d3.selectAll(".dialogue-tbl-progress>div").style("background-color", function() { return progressScale(d3.select(this).html()); });
      </script>
  `,
})
export class AppComponent  {  }