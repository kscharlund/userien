% for class_name, class_results in scores.items():
<p style="font-weight: bold">{{class_name}}</p>
<table>
% for result in class_results:
<tr><td>{{result["name"]}}, {{result["team"]}}</td><td>{{result["score"]}}</td></tr>
% end
</table>
% end
