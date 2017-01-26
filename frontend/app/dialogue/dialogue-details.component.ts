import { Component, Input } from '@angular/core';

import { Call } from '../models';

@Component({
  selector: 'dialogue-details',
  template: `
<div class="dialogue-details container-fluid">
	<div class="row">
		<div class="col-sm">
			<h3>Основные проблемы разговора</h3>
			<div class = "dialogue-info">
				<table>
					<tbody>
						<tr class="dialogue-info-group">
							<td colspan="2"><img src="img/close.png" alt="show" />Количественно-временные параметры</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="8" aria-valuemin="0" aria-valuemax="10" style="width:80%"></div>
								</div>
							</td>
							<td>8 баллов</td>
						</tr>
						<tr>
							<td>Речь оператора</td>
							<td>70%</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="10" style="width:20%"></div>
								</div>
							</td>
							<td>2 балла</td>
						</tr>
						<tr>
							<td>Речь клиента</td><!--завичимые параметры может как-то отметить. Строго говоря речь клиента оценивать не имеет смысла-->
							<td>30%</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="4" aria-valuemin="0" aria-valuemax="10" style="width:40%"></div>
								</div>
							</td>
							<td>4 балла</td>
						</tr>
						<tr>
							<td>Речь оператора</td>
							<td>00:24</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="6" aria-valuemin="0" aria-valuemax="10" style="width:60%"></div>
								</div>
							</td>
							<td>6 баллов</td>
						</tr>
						<tr>
							<td>Количество переводов</td>
							<td>15 шт</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="10" aria-valuemin="0" aria-valuemax="10" style="width:100%"></div>
								</div>
							</td>
							<td>10 баллов</td>
						</tr>
						<tr>
							<td>Количество удержаний</td>
							<td>2 шт</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="10" style="width:00%"></div>
								</div>
							</td>
							<td>0 баллов</td>
						</tr>
						<tr>
							<td>Макс. время удержания</td>
							<td>00:59</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="7" aria-valuemin="0" aria-valuemax="10" style="width:70%"></div>
								</div>
							</td>
							<td>7 баллов</td>
						</tr>
						<tr>
							<td>Общее время удержаний</td>
							<td>20:02</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="8" aria-valuemin="0" aria-valuemax="10" style="width:80%"></div>
								</div>
							</td>
							<td>8 баллов</td>
						</tr>
						<tr class="dialogue-info-group">
							<td colspan="2"><img src="img/open.png" alt="show" />Параметры речевой активности</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="1" aria-valuemin="0" aria-valuemax="10" style="width:10%"></div>
								</div>
							</td>
							<td>1 балл</td>
						</tr>
						<tr class="dialogue-info-group">
							<td colspan="2"><img src="img/open.png" alt="show" />Лексико-семантический анализ</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="9" aria-valuemin="0" aria-valuemax="10" style="width:90%"></div>
								</div>
							</td>
							<td>9 баллов</td>
						</tr>
						<tr class="dialogue-info-group">
							<td colspan="2"><img src="img/open.png" alt="show" />Эмоциональное состояние</td>
							<td>
								<div class="progress dialogue-info-progress">
									<div class="progress-bar" role="progressbar" aria-valuenow="8" aria-valuemin="0" aria-valuemax="10" style="width:80%"></div>
								</div>
							</td>
							<td>8 баллов</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
		<div class="col-sm">
			<h3>Запись звонка</h3>
			<div style="height:187px;"> 
			<audio controls preload>
				<source src="#">
			</audio>
			</div>
			<h3>Расшифровка диалога</h3>
			<div class="dialogue-script">
				<table>
					<tbody>
						<tr>
							<td class="dialogue-script-op">Оператор:</td>
							<td>Здравствуйте! вы насчет работы торговым представителем?</td>
						</tr>
						<tr>
							<td class="dialogue-script-cl">Клиент:</td>
							<td>Да, вот моё резюме.</td>
						</tr>
						<tr>
							<td class="dialogue-script-op">Оператор:</td>
							<td>В нашей компании ассортимент товаров, с которыми вам придется работать, будет намного шире. Это кондитерские изделия: торты, пирожные, рулетики, конфеты. На какую зарплату вы рассчитываете?</td>
						</tr>
						<tr>
							<td class="dialogue-script-cl">Клиент:</td>
							<td>На пятьсот долларов, как указано в вашем объявлении. Еще я рассчитываю, что если буду хорошо справляться со своими обязанностями, моя зарплата вырастет.</td>
						</tr>
						<tr>
							<td class="dialogue-script-op">Оператор:</td>
							<td>Наша компания всегда поощряет сотрудников за успехи в труде. Скажите, почему вы выбрали для работы именно нашу компанию?</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
<div class="dialogue-details-bottom"></div>`,
	styleUrls: ["app/dialogue/dialogue-details.component.css"]
})
export class DialogueDetailsComponent  {
	@Input() call : Call;
}
