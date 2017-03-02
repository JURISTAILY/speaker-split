import { Pipe, PipeTransform } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common'
@Pipe({
  name: 'nanUniformer'
})
export class NaNUniformerPipe implements PipeTransform {

  transform(value: string): string {
  	if (isNaN(parseFloat(value))) {
  		return "—";
  	}
    return value;
  }

  static TRANSFORMER = {
  	decimal : new DecimalPipe('rus'),
  	uniformer : new NaNUniformerPipe(),
  	transform(num : number) : string {
  	  return this.uniformer.transform(this.decimal.transform(num));
  	}
  }

  static PERCENT_TANSFORMER = {
    perc : new PercentPipe('rus'),
    transform(num : number) : string {
      if (isFinite(num)) {
        return this.perc.transform(num);
      }
      return "—";
    }
  }
}
