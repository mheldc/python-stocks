use stocks_db
go

drop table stock_data
go

create table stock_data
(
	id uniqueidentifier primary key default newid(),
	code nvarchar(10) not null,
	[date] datetime not null,
	[open] decimal(10, 6) not null default 0,
	[close] decimal(10, 6) not null default 0,
	[high] decimal(10, 6) not null default 0,
	[low] decimal(10, 6) not null default 0,
	[adj_close] decimal(10, 6) not null default 0,
	[volume] float not null default 0,
	ingestion_date datetime not null default getdate()
)
go


If Exists (select OBJECT_ID('sp_upsert_stock_data', 'P'))
	Drop Procedure sp_upsert_stock_data
go

create procedure sp_upsert_stock_data
(
	@stock_code nvarchar(10),
	@stock_date datetime,
	@stock_open decimal(10, 6),
	@stock_high decimal(10, 6),
	@stock_low decimal(10, 6),
	@stock_close decimal(10, 6),
	@stock_adj_close decimal(10, 6),
	@stock_volume float
)
As
	Begin

		/*
			-- Logic
			1. Update all values except for stock_data code and date if the data pertaining to @stock_code and @stock_date already exists.
			2. Append/insert data if @stock_code and @stock_date does not exists.
		*/

		If Exists (Select [date] From stock_data Where [code] = @stock_code and [date] = @stock_date)
			Update stock_data
			Set [open] = @stock_open, [close] = @stock_close, [adj_close] = @stock_adj_close, [high] = @stock_high, [low] = @stock_low, [volume] = @stock_volume
			Where [code] = @stock_code and [date] = @stock_date

		Else
			Insert Into stock_data
				([code], [date], [open], [close], [adj_close], [high], [low], [volume])
			Values
				(@stock_code, @stock_date, @stock_open, @stock_close, @stock_adj_close, @stock_high, @stock_low, @stock_volume)
			
	End
go