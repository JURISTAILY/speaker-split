"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var CALLS = [
    {
        id: "#0157",
        duration: 545,
        sa: 123,
        operatorSpeechDuration: 123,
        clientInterruptions: 3,
        operatorInterruptions: 34,
        operatorSilenceDuration: 441,
        legibility: 80,
        isIncoming: true,
        grade: 8,
        transcripts: []
    },
    {
        id: "#0158",
        duration: 1235,
        sa: 154323,
        operatorSpeechDuration: 312542,
        clientInterruptions: 351234,
        operatorInterruptions: 34143,
        operatorSilenceDuration: 4312423,
        legibility: 35,
        isIncoming: false,
        grade: 4,
        transcripts: []
    },
    {
        id: "#0159",
        duration: 545,
        sa: 123,
        operatorSpeechDuration: 123,
        clientInterruptions: 3,
        operatorInterruptions: 34,
        operatorSilenceDuration: 441,
        legibility: 99,
        isIncoming: true,
        grade: 5,
        transcripts: []
    }
];
var DialogueViewComponent = (function () {
    function DialogueViewComponent() {
        this.calls = CALLS;
    }
    DialogueViewComponent = __decorate([
        core_1.Component({
            selector: 'dialogue-view',
            template: "<table class=\"dialogue-view\">\n\t<thead>\n\t\t<tr>\n\t\t\t<td>\u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u0441\u0440\u0435\u0437\u0430</td>\n\t\t\t<td>\u0414\u043B\u0438\u0442\u0435\u043B\u044C\u043D\u043E\u0441\u0442\u044C \u0440\u0430\u0437\u0433\u043E\u0432\u043E\u0440\u0430</td>\n\t\t\t<td class=\"dialogue-sa\">\n\t\t\t\tSA<img src=\"img/interrogatory.png\" alt=\"interrogatory\" title=\"Tooltip on right\" />\n\t\t\t</td>\n\t\t\t<td>\u0414\u043E\u043B\u044F \u0440\u0435\u0447\u0438 \u043E\u043F\u0435\u0440\u0430\u0442\u043E\u0440\u0430</td>\n\t\t\t<td>\u0414\u043B\u0438\u0442\u0435\u043B\u044C\u043D\u043E\u0441\u0442\u044C \u0440\u0435\u0447\u0438 \u043E\u043F\u0435\u0440\u0430\u0442\u043E\u0440\u0430</td>\n\t\t\t<td>\u041A\u043B\u0438\u0435\u043D\u0442 \u043F\u0435\u0440\u0435\u0431\u0438\u0432\u0430\u0435\u0442 \u043E\u043F\u0435\u0440\u0430\u0442\u043E\u0440\u0430</td>\n\t\t\t<td>\u041E\u043F\u0435\u0440\u0430\u0442\u043E\u0440 \u043F\u0435\u0440\u0435\u0431\u0438\u0432\u0430\u0435\u0442 \u043A\u043B\u0438\u0435\u043D\u0442\u0430</td>\n\t\t\t<td>\u041C\u043E\u043B\u0447\u0430\u043D\u0438\u0435 \u043E\u043F\u0435\u0440\u0430\u0442\u043E\u0440\u0430</td>\n\t\t\t<td>\u0420\u0430\u0437\u0431\u043E\u0440\u0447\u0438\u0432\u043E\u0441\u0442\u044C \u0440\u0435\u0447\u0438 \u043E\u043F\u0435\u0440\u0430\u0442\u043E\u0440\u0430</td>\n\t\t\t<td>\u0422\u0438\u043F</td>\n\t\t\t<td>\u041E\u0446\u0435\u043D\u043A\u0430 \u0440\u0430\u0437\u0433\u043E\u0432\u043E\u0440\u0430</td>\n\t\t\t<td>\u0417\u0430\u043F\u0438\u0441\u044C \u0440\u0430\u0437\u0433\u043E\u0432\u043E\u0440\u0430</td>\n\t\t</tr>\n\t</thead>\n\t<tbody dialogue-item *ngFor=\"let call of calls\" [call]=\"call\">\n\t</tbody>\n</table>\n\u0442\u0443\u0442 \u0441\u043A\u0430\u0447\u0430\u044E .xls",
            styleUrls: ["app/dialogue/dialogue-view.component.css"],
            encapsulation: core_1.ViewEncapsulation.None
        }), 
        __metadata('design:paramtypes', [])
    ], DialogueViewComponent);
    return DialogueViewComponent;
}());
exports.DialogueViewComponent = DialogueViewComponent;
//# sourceMappingURL=dialogue-view.component.js.map