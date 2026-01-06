use anchor_lang::prelude::*;
declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod bank {
    use super::*;
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        // !!! 漏洞点：直接动了账户里的钱，但根本没检查账户所有人有没有签名 !!!
        let from = &mut ctx.accounts.from;
        let to = &mut ctx.accounts.to;
        **from.to_account_info().try_borrow_mut_lamports()? -= amount;
        **to.to_account_info().try_borrow_mut_lamports()? += amount;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    /// CHECK: Unsafe - 这里本应该用 Signer 但用了 AccountInfo
    #[account(mut)]
    pub from: AccountInfo<'info>, 
    #[account(mut)]
    pub to: AccountInfo<'info>, 
    pub system_program: Program<'info, System>,
}
