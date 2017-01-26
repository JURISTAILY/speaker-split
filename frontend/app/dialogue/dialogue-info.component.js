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
var models_1 = require('../models');
var DialogueInfoComponent = (function () {
    function DialogueInfoComponent() {
    }
    __decorate([
        core_1.Input(), 
        __metadata('design:type', models_1.Info)
    ], DialogueInfoComponent.prototype, "info", void 0);
    DialogueInfoComponent = __decorate([
        core_1.Component({
            selector: '[dialogue-info]',
            template: "\n<tr>\n\t<td>{{ call.id }}</td>\n\t<td>{{ call.duration }}</td>\n\t<td>{{ call.sa }}</td>\n\t<td>{{ (call.operatorSpeechDuration / call.duration * 1000) / 10 | number: '1.1-1' }}%</td>\n\t<td>{{ call.operatorSpeechDuration }}</td>\n\t<td>{{ call.clientInterruptions }}</td>\n\t<td>{{ call.operatorInterruptions }}</td>\n\t<td>{{ call.operatorSilenceDuration }}</td>\n\t<td>{{ call.legibility }}%</td>\n\n\t<td><div [class.incoming]=\"call.isIncoming\" [class.outgoing]=\"!call.isIncoming\"></div></td>\n\n\t<td><div class=\"dialogue-tbl-progress\"><div>{{ call.grade }}</div></div></td>\n\t<td><span class=\"dialogue-tbl-info-trigger\" (click)=\"switchDetails()\">{{ (open ? \"\u0421\u0432\u0435\u0440\u043D\u0443\u0442\u044C\" : \"\u0420\u0430\u0437\u0432\u0435\u0440\u043D\u0443\u0442\u044C\") }}</span></td>\n</tr>\n<tr *ngIf=\"open\">\n\t<td colspan=\"12\">\n\t\t<dialogue-details [call]=\"call\"></dialogue-details>\n\t</td>\n</tr>\n"
        }), 
        __metadata('design:paramtypes', [])
    ], DialogueInfoComponent);
    return DialogueInfoComponent;
}());
exports.DialogueInfoComponent = DialogueInfoComponent;
//# sourceMappingURL=dialogue-info.component.js.map