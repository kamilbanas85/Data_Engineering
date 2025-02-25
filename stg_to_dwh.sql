/****** procedure take data from stg table and put into dwh layer with removing ' ', '(', ')', '-' from columns name ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [stg].[sp_insert_from_stg_to_dwh]
    @SourceTable NVARCHAR(MAX),
    @TargetTable NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @columns_org NVARCHAR(MAX);
    DECLARE @columns_modified NVARCHAR(MAX);
    DECLARE @sql NVARCHAR(MAX);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Generate the original column list
        SELECT @columns_org = STRING_AGG(QUOTENAME(name), ', ')
        FROM sys.columns
        WHERE object_id = OBJECT_ID(@SourceTable);

        -- Generate the modified column list (replace spaces with underscores)
		SELECT @columns_modified = STRING_AGG(QUOTENAME(REPLACE(REPLACE(REPLACE(REPLACE(name, ' ', '_'), '-', ''), '(', ''), ')', '')), ', ')
		FROM sys.columns
        WHERE object_id = OBJECT_ID(@TargetTable);

        -- Construct the SQL to truncate the destination table
        SET @sql = 'TRUNCATE TABLE ' + @TargetTable + ';';
        EXEC sp_executesql @sql;

        -- Construct the SQL to copy data
        SET @sql = '
            INSERT INTO ' + @TargetTable + ' (' + @columns_modified + ')
            SELECT ' + @columns_org + '
            FROM ' + @SourceTable + ';';

        -- Execute the dynamic SQL
        EXEC sp_executesql @sql;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;

        -- Print error details
        PRINT 'Error Number: ' + CAST(ERROR_NUMBER() AS NVARCHAR(10));
        PRINT 'Error Message: ' + ERROR_MESSAGE();
        PRINT 'Error Line: ' + CAST(ERROR_LINE() AS NVARCHAR(10));
    END CATCH;
END;
GO


