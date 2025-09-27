<html>

<head>
    <title>Resultat, {{event_name}}</title>
    <style>
    td, th {
        padding: 0.1em 0.3em;
    }
    .unfinished {
        color: #666;
        background: #ddd;
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
            <th>Antal tävlingar</th>
            <th>Fjärde resultat</th>
            <th>Femte resultat</th>
        </tr>
        % for result in results:
        <tr class="{{'unfinished' if result['unfinished'] else 'finished'}}">
            <td>{{result["name"]}}</td>
            <td>{{result["team"]}}</td>
            <td>{{result.get("current_score", "")}}</td>
            <td>{{result["total_score"]}}</td>
            <td>{{result["num_competitions"]}}</td>
            <td>{{result["fourth_score"]}}</td>
            <td>{{result["fifth_score"]}}</td>
        </tr>
        % end
    </table>
    % end

    % for series in previous_competitions:
    <p>
        % for event_id, event_name in series:
        <a href="{{event_id}}">{{event_name}}</a><br/>
        % end
    </p>
    % end
</body>

</html>