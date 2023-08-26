<html>

<head>
    <title>Resultat, {{event_name}}</title>
    <style>
    td, th {
        padding: 0.1em 0.3em;
    }
    </style>
</head>

<body>
    <h1>Resultat, {{event_name}}</h1>
    % for class_name, results in result_tables.items():
    <p style="font-weight: bold">{{class_name}}</p>
    <table>
        <tr>
            <th>Namn</th>
            <th>Klubb</th>
            <th>Poäng</th>
            <th>Poäng, totalt</th>
        </tr>
        % for result in results:
        <tr>
            <td>{{result["name"]}}</td>
            <td>{{result["team"]}}</td>
            <td>{{result.get("current_score", "")}}</td>
            <td>{{result["total_score"]}}</td>
        </tr>
        % end
    </table>
    % end
</body>

</html>