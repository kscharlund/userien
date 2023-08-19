<html>

<head>
    <title>Resultat, {{event_name}}</title>
</head>

<body>
    <h1>Resultat, {{event_name}}</h1>
    % for class_name, class_results in scores.items():
    <p style="font-weight: bold">{{class_name}}</p>
    <table>
        % for result in class_results:
        <tr>
            <td>{{result["name"]}}, {{result["team"]}}</td>
            <td>{{result["score"]}}</td>
        </tr>
        % end
    </table>
    % end
</body>

</html>