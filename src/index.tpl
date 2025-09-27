<html>

<head>
    <title>Resultaträknare, Ungdomsserien i Linköping</title>
</head>

<body>
    <h1>Resultaträknare, Ungdomsserien i Linköping</h1>
    <form action="results" method="post" enctype="multipart/form-data">
        Resultat-fil i IOF XML-format: <input type="file" name="result_file" />
        <input type="submit" value="Ladda upp" />
    </form>

    % for series in previous_competitions:
    <p>
        % for event_id, event_name in series:
        <a href="result/{{event_id}}">{{event_name}}</a><br/>
        % end
    </p>
    % end
</body>

</html>