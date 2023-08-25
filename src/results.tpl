<html>

<head>
    <title>Resultat, {{event_name}}</title>
</head>

<body>
    <h1>Resultat, {{event_name}}</h1>
    % for class_result in class_results:
    <p style="font-weight: bold">{{class_result["class_name"]}}</p>
    <table>
        % for result in class_result["results"]:
        <tr>
            <td>{{result["person_name"]}}, {{result["team"]}}</td>
            <td>{{result["score"]}}</td>
        </tr>
        % end
    </table>
    % end
</body>

</html>